# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import api, models, _
from odoo.exceptions import ValidationError
from odoo.tools.config import config
from lxml import etree
from odoo.osv.orm import setup_modifiers


_logger = logging.getLogger(__name__)


class ServerEnvMixin(models.AbstractModel):
    _inherit = "server.env.mixin"

    def _compute_server_env_from_default(self, field_name, options):
        """ First return database encrypted value then default value """
        self.ensure_one()
        encrypted_data_name = "%s,%s" % (self._name, self.id)
        env = self.env.context.get("environment", None)
        vals = (
            self.env["encrypted.data"]
            .sudo()
            ._encrypted_read_json(encrypted_data_name, env=env)
        )
        if vals.get(field_name):
            self[field_name] = vals[field_name]
        else:
            return super()._compute_server_env_from_default(
                field_name, options
            )

    def _inverse_server_env(self, field_name):
        """
            When this module is installed, we store values into encrypted data
            env instead of a default field in database (not env dependent).
        """
        is_editable_field = self._server_env_is_editable_fieldname(field_name)
        encrypted_data_obj = self.env["encrypted.data"].sudo()
        env = self.env.context.get("environment", None)
        for record in self:
            if record[is_editable_field]:
                encrypted_data_name = "%s,%s" % (record._name, record.id)
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
            action = self.env["ir.actions.act_window"].browse(
                action_id).read()[0]
            action["view_mode"] = "form"
        action["res_id"] = self.id
        views_form = []
        for view_id, view_type in action.get("views", []):
            if view_type == "form":
                views_form.append((view_id, view_type))
        action["views"] = views_form
        return action

    def _get_extra_environment_info_div(self, current_env, extra_envs):
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
        alert_string = _("Modify values for {} environment").format(
            current_env
        )
        alert_type = (
            current_env == config.get("running_env")
            and "alert-info"
            or "alert-warning"
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
            setup_modifiers(field, self.fields_get(field_name))

    def _update_form_view_from_env(self, arch, view_type):
        if view_type != "form":
            return arch
        current_env = self.env.context.get("environment") or config.get(
            "running_env"
        )
        # Important to keep this list sorted. It makes sure the button to
        # switch environment will always be in the same order. (more user
        # friendly) and the test would fail without it as the order could
        # change randomly and the view would then also change randomly
        other_environments = sorted([
            key[15:]
            for key, val in config.options.items()
            if key.startswith("encryption_key_")
            and val
            and key[15:] != current_env
        ])

        if not current_env:
            raise ValidationError(
                _(
                    "you need to define the running_env entry in your odoo "
                    "configuration file"
                )
            )
        doc = etree.XML(arch)
        node = doc.xpath("//sheet")
        if node:
            node = node[0]
            elem = self._get_extra_environment_info_div(
                current_env, other_environments
            )
            node.insert(0, elem)

            if current_env != config.get("running_env"):
                self._set_readonly_form_view(doc)
            arch = etree.tostring(doc, pretty_print=True, encoding="unicode")
        else:
            _logger.error(
                "Missing sheet for form view on object {}".format(self._name)
            )
        return arch

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )
        res["arch"] = self._update_form_view_from_env(res["arch"], view_type)
        return res
