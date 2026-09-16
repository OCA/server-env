# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AuthOAuthProvider(models.Model):
    _name = "auth.oauth.provider"
    _inherit = ["auth.oauth.provider", "server.env.techname.mixin", "server.env.mixin"]

    enabled = fields.Boolean(search="_search_enabled")

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        oauth_fields = {
            "client_id": {},
            "enabled": {},
        }
        oauth_fields.update(base_fields)
        return oauth_fields

    @api.model
    def _server_env_global_section_name(self):
        return "auth_oauth"

    @api.model
    def _search_enabled(self, operator, value):
        if operator not in ["=", "!="] or not isinstance(value, bool):
            raise UserError(_("Operation not supported"))
        if operator != "=":
            value = not value
        enabled = self.search([]).filtered(lambda p: p.enabled)
        return [("id", "in" if value else "not in", enabled.ids)]
