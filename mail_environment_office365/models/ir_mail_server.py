# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Anna Janiszewska <anna.janiszewska@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        office365_fields = {
            "smtp_authentication": {},
        }
        office365_fields.update(base_fields)
        return office365_fields
