# Copyright 2026 Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class PaymentProvider(models.Model):
    _name = "payment.provider"
    _inherit = ["payment.provider", "server.env.mixin"]

    _server_env_section_name_field = "code"

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        stripe_fields = {
            "stripe_publishable_key": {},
            "stripe_secret_key": {},
            "stripe_webhook_secret": {},
        }
        stripe_fields.update(base_fields)
        return stripe_fields

    @api.model
    def _server_env_global_section_name(self):
        return "payment_provider"

    def _server_env_add_default_field(self, base_field):
        # required_if_provider is an attribute of fields in payments modules
        # _server_env_add_default_field copies all the fields, required_if_provider
        # included. We don't want it for default fields
        res = super()._server_env_add_default_field(base_field)
        fieldname = self._server_env_default_fieldname(base_field.name)
        field = self._fields.get(fieldname)
        if field and getattr(field, "required_if_provider", None):
            if field.args:
                field.args.pop("required_if_provider", None)
            field.required_if_provider = None
        return res

    def _check_required_if_provider(self):
        # bypass validation for our install hook
        if self.env.context.get("strip_env_skip_check_required_if_provider"):
            return
        return super()._check_required_if_provider()
