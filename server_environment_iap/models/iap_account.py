# Copyright 2021 Camptocamp SA <https://www.camptocamp.com/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class IapAccount(models.Model):
    _name = "iap.account"
    _inherit = [
        "iap.account",
        "server.env.techname.mixin",
        "server.env.mixin",
    ]

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        iap_fields = {
            "service_name": {},
            "account_token": {},
        }
        iap_fields.update(base_fields)
        return iap_fields

    @api.model
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files

        Can be customized in your model
        """
        return "iap_account"
