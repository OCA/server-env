# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from lxml import etree

from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools.config import config

_logger = logging.getLogger(__name__)


class ServerEnvMixin(models.AbstractModel):
    _inherit = "server.env.mixin"

    def _current_env_encrypted_key_exists(self):
        env = self.env["encrypted.data"]._retrieve_env()
        key_name = f"encryption_key_{env}"
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

    @api.depends_context("environment")
    def _compute_server_env(self):
        return super()._compute_server_env()

    def _compute_server_env_from_default(self, field_name, options):
        """First return database encrypted value then default value"""
        # in case of bad configuration (no encryption key for current env) the module
        # is useless, we do fallback directly on serven_environement behavior
        if not self._current_env_encrypted_key_exists():
            return super()._compute_server_env_from_default(field_name, options)
        encrypted_data_name = f"{self._name},{self.id}"
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
                encrypted_data_name = f"{record._name},{record.id}"
                values = encrypted_data_obj._encrypted_read_json(
                    encrypted_data_name, env=env
                )
                new_val = {field_name: record[field_name]}
                values.update(new_val)
                encrypted_data_obj._encrypted_store_json(
                    encrypted_data_name, values, env=env
                )
                # The env fields are non-stored computed fields with no field
                # dependency on the storage. Their cache is therefore not
                # updated when we store here: refresh the *sibling* fields from
                # the values we just wrote, so that a constraint validating a
                # sibling field (e.g. microsoft_outlook reading smtp_encryption
                # while saving smtp_authentication) sees the current values.
                # The written field is left untouched so later inverses of the
                # same write still read its freshly-assigned value.
                record._update_cache(
                    {
                        name: value
                        for name, value in values.items()
                        if (
                            name in record._fields
                            and name != field_name
                            and not record.env.cache.contains(
                                record, record._fields[name]
                            )
                        )
                    }
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

    def _get_extra_environment_info_div(self, current_env, all_environments):
        # if the module configuration is missing (no current env encryption key)
        # display a warning instead as the module has no effect.
        if not self._current_env_encrypted_key_exists():
            button_div = "<div>"
            warning_string = self.env._(
                "The encryption key for current environement is not defined"
            )
            elem = etree.fromstring(
                """
                  <div class="d-flex justify-content-between">
                  <div class="alert lead {} text-center d-inline">
                      <strong>{}</strong>
                    </div>
                  </div>
            """.format("alert-danger", warning_string)
            )
            return elem

        elem_string = """<div class="d-flex justify-content-between">"""
        for environment in all_environments:
            alert_type = (
                environment == config.get("running_env")
                and "alert-info"
                or "alert-warning"
            )
            alert_string = self.env._("Modify values for {} environment").format(
                environment
            )
            elem_string += f"""
              <div class="alert lead {alert_type} text-center d-inline"
            invisible="context.get('environment', '{current_env}') != '{environment}'">
                  <strong>{alert_string}</strong>
              </div>
            """
        button_div = """<div class="d-flex gap-1 flex-wrap align-items-center">"""
        button_string = self.env._("Define values for ")
        for environment in all_environments:
            button = """
            <button name="action_change_env_data_encrypted_fields"
                    type="object" string="{}{}"
                    class="btn btn-lg btn-primary ml-2"
                    invisible="context.get('environment', '{}') == '{}'"
                    context="{}"/>
            """.format(
                button_string,
                environment,
                current_env,
                environment,
                {"environment": environment},
            )
            button_div += f"{button}"
        button_div += "</div>"
        elem_string += button_div
        elem_string += "</div>"
        elem = etree.fromstring(elem_string)
        return elem

    def _set_button_invisible_form_view(self, doc, current_env, all_environments):
        """
        Hide button from view when we are in the context of an environment different
        than the running one.
        """
        invisible_condition = (
            f"""context.get("environment", '{current_env}') != '{current_env}'"""
        )
        for button in doc.iter("button"):
            button.attrib["invisible"] = invisible_condition

    def _set_readonly_form_view(self, doc, current_env, all_environments):
        readonly_condition = (
            f"""context.get("environment", '{current_env}') != '{current_env}'"""
        )
        for field in doc.iter("field"):
            env_fields = self._server_env_fields.keys()
            field_name = field.get("name")
            if field_name in env_fields:
                continue
            current_readonly_cond = field.attrib.get("readonly", "")
            current_readonly_cond = (
                current_readonly_cond
                and f"({current_readonly_cond}) or {readonly_condition}"
                or f"{readonly_condition}"
            )
            field.attrib["readonly"] = current_readonly_cond

    def _update_form_view_from_env(self, arch, view_type):
        if view_type != "form":
            return arch
        current_env = self.env.context.get("environment") or config.get("running_env")

        if not current_env:
            raise ValidationError(
                self.env._(
                    "you need to define the running_env entry in your odoo "
                    "configuration file"
                )
            )
        current_env = config.get("running_env")
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
        all_environments = other_environments.copy()
        all_environments.insert(0, current_env)

        node = arch.xpath("//sheet")
        if node:
            self._set_button_invisible_form_view(arch, current_env, all_environments)
            self._set_readonly_form_view(arch, current_env, all_environments)
            node = node[0]
            elem = self._get_extra_environment_info_div(current_env, all_environments)
            node.insert(0, elem)
        else:
            _logger.error(f"Missing sheet for form view on object {self._name}")
        return arch

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        arch, view = super()._get_view(view_id=view_id, view_type=view_type, **options)
        arch = self._update_form_view_from_env(arch, view_type)
        return arch, view
