# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, models


class AuthOAuthProvider(models.Model):
    _name = "auth.oauth.provider"
    _inherit = ["auth.oauth.provider", "server.env.techname.mixin", "server.env.mixin"]

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
