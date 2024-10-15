# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        gmail_fields = {
            "google_gmail_authorization_code": {},
            "google_gmail_refresh_token": {},
        }
        gmail_fields.update(base_fields)
        return gmail_fields
