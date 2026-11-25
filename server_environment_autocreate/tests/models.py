# Copyright 2024 XCG Consulting
# @author Vincent Hatakeyama
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ExternalService(models.Model):
    _name = "external_service"
    _description = "External Service"
    _inherit = "server.env.mixin"

    name = fields.Char(required=True)
    description = fields.Char(required=True)
    host = fields.Char()
    user = fields.Char()
    password = fields.Char()

    @property
    def _server_env_fields(self):
        return {
            "host": {},
            "user": {},
            "password": {},
        }


class ExternalService2(models.Model):
    _name = "external_service_2"
    _inherit = "external_service"
    _description = "External Service 2"
    _server_env_allow_autocreate = False
