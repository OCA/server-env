# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
import logging

from lxml import etree

from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools.config import config

_logger = logging.getLogger(__name__)


class ServerEnvMixin(models.AbstractModel):
    _inherit = "server.env.mixin"

    def _current_env_encrypted_key_exists(self):
        env = self.env["encrypted.data"]._retrieve_env()
        key_name = "encryption_key_%s" % env
        key_str = config.get(key_name)
        key_exists = key_str and True or False
        if not key_exists:
            logging.warning(
                "The minimal configuration is missing. You need at least to add an "
                "encryption key for the current environment  : %s. While the "
                "configuration is missing, the module has no effect",
                env,
            )
        return key_exists

    def _compute_server_env_from_default(self, field_name, options):
        """First return database encrypted value then default value"""
        # in case of bad configuration (no encryption key for current env) the module
        # is useless, we do fallback directly on serven_environement behavior
        if not self._current_env_encrypted_key_exists():
            return super()._compute_server_env_from_default(field_name, options)
        encrypted_data_name = "{},{}".format(self._name, self.id)
        env = self.env.context.get("environment", None)

        vals = (
            self.env["encrypted.data"]
            .sudo()
            ._encrypted_read_json(encrypted_data_name, env=env)
        )
        if vals.get(field_name):
            self[field_name] = vals[field_name]
        else:
            return super()._compute_server_env_from_default(field_name, options)

    def _inverse_server_env(self, field_name):
        """
        When this module is installed, we store values into encrypted data
        env instead of a default field in database (not env dependent).
        """
        # in case of bad configuration (no encryption key for current env) the module
        # is useless, we do fallback directly on serven_environement behavior
        if not self._current_env_encrypted_key_exists():
            return super()._inverse_server_env(field_name)
        is_editable_field = self._server_env_is_editable_fieldname(field_name)
        encrypted_data_obj = self.env["encrypted.data"].sudo()
        env = self.env.context.get("environment", None)
        for record in self:
            if record[is_editable_field]:
                encrypted_data_name = "{},{}".format(record._name, record.id)
                values = encrypted_data_obj._encrypted_read_json(
                    encrypted_data_name, env=env
                )
                new_val = {field_name: record[field_name]}
                values.update(new_val)
                encrypted_data_obj._encrypted_store_json(
                    encrypted_data_name, values, env=env
                )

    def action_change_env_data_encrypted_fields(self):
        action_id = self.env.context.get("params", {}).get("action")
        if not action_id:
            # We don't know which action we are using... take default one
            action = self.get_formview_action()
        else:
            action = (
                self.env["ir.actions.act_window"].browse(action_id).sudo().read()[0]
            )
            action["view_mode"] = "form"
        action["res_id"] = self.id
        views_form = []
        for view_id, view_type in action.get("views", []):
            if view_type == "form":
                views_form.append((view_id, view_type))
        action["views"] = views_form
        return action

    def _get_extra_environment_info_div(self, current_env, extra_envs):
        # if the module configuration is missing (no current env encryption key)
        # display a warning instead as the module has no effect.
        if not self._current_env_encrypted_key_exists():
            button_div = "<div>"
            warning_string = _(
                "The encryption key for current environement is not defined"
            )
            elem = etree.fromstring(
                """
                  <div class="d-flex justify-content-between">
                  <div class="alert lead {} text-center d-inline">
                      <strong>{}</strong>
                    </div>
                  </div>
            """.format(
                    "alert-danger", warning_string
                )
            )
            return elem

        # TODO we could use a qweb template here
        button_div = "<div>"
        button_string = _("Define values for ")
        for environment in extra_envs:
            button = """
            <button name="action_change_env_data_encrypted_fields"
                    type="object" string="{}{}"
                    class="btn btn-lg btn-primary ml-2"
                    context="{}"/>
            """.format(
                button_string, environment, {"environment": environment}
            )
            button_div += "{}".format(button)
        button_div += "</div>"
        alert_string = _("Modify values for {} environment").format(current_env)
        alert_type = (
            current_env == config.get("running_env") and "alert-info" or "alert-warning"
        )
        elem = etree.fromstring(
            """
              <div class="d-flex justify-content-between">
              <div class="alert lead {} text-center d-inline">
                  <strong>{}</strong>
                </div>
                {}
              </div>
        """.format(
                alert_type, alert_string, button_div
            )
        )
        return elem

    def _set_readonly_form_view(self, doc):
        for field in doc.iter("field"):
            env_fields = self._server_env_fields.keys()
            field_name = field.get("name")
            if field_name in env_fields:
                continue
            field.set("readonly", "1")
            field.set("modifiers", json.dumps({"readonly": True}))

    def _update_form_view_from_env(self, arch, view_type):
        if view_type != "form":
            return arch
        current_env = self.env.context.get("environment") or config.get("running_env")
        # Important to keep this list sorted. It makes sure the button to
        # switch environment will always be in the same order. (more user
        # friendly) and the test would fail without it as the order could
        # change randomly and the view would then also change randomly
        other_environments = sorted(
            [
                key[15:]
                for key, val in config.options.items()
                if key.startswith("encryption_key_") and val and key[15:] != current_env
            ]
        )

        if not current_env:
            raise ValidationError(
                _(
                    "you need to define the running_env entry in your odoo "
                    "configuration file"
                )
            )
        node = arch.xpath("//sheet")
        if node:
            node = node[0]
            elem = self._get_extra_environment_info_div(current_env, other_environments)
            node.insert(0, elem)

            if current_env != config.get("running_env"):
                self._set_readonly_form_view(arch)
        else:
            _logger.error("Missing sheet for form view on object {}".format(self._name))
        return arch

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        arch, view = super()._get_view(view_id=view_id, view_type=view_type, **options)
        arch = self._update_form_view_from_env(arch, view_type)
        return arch, view

    def _get_view_cache_key(self, view_id=None, view_type="form", **options):
        res = super()._get_view_cache_key(
            view_id=view_id, view_type=view_type, **options
        )
        res += (self.env.context.get("environment", False),)
        return res
