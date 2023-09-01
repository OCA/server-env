# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class FetchmailServer(models.Model):
    _inherit = "fetchmail.server"

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        office365_fields = {
            "use_microsoft_outlook_service": {},
        }
        office365_fields.update(base_fields)
        return office365_fields
