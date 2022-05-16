# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class IapAccount(models.Model):
    _inherit = ["iap.account", "server.env.mixin"]
    _name = "iap.account"

    @property
    def _server_env_fields(self):
        return {
            "provider": {},
            "account_token": {},
        }
