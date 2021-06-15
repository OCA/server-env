# Copyright 2021 Camptocamp SA <https://www.camptocamp.com/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class AuthSamlProvider(models.Model):
    _name = "auth.saml.provider"
    _inherit = ["auth.saml.provider", "server.env.mixin"]

    sp_pem_public_path = fields.Char(
        string="sp_pem_public_path env config value",
    )

    sp_pem_private_path = fields.Char(
        string="sp_pem_private_path env config value",
    )

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        auth_saml_fields = {
            "idp_metadata": {},
            "sp_baseurl": {},
            "sp_pem_public_path": {},
            "sp_pem_private_path": {},
        }
        auth_saml_fields.update(base_fields)
        return auth_saml_fields

    @api.model
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files
        Can be customized in your model
        """
        return "auth_saml_provider"

    def _get_cert_key_path(self, field="sp_pem_public"):
        # If the setup is done in env, we want to bypass the base method
        if self.sp_pem_public_path and field == "sp_pem_public":
            return self.sp_pem_public_path
        if self.sp_pem_private_path and field == "sp_pem_private":
            return self.sp_pem_private_path
        return super()._get_cert_key_path(field)
