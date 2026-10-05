# Copyright 2012-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class IrMailServer(models.Model):
    _name = "ir.mail_server"
    _inherit = ["ir.mail_server", "server.env.mixin"]  # noqa: RUF012

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        mail_fields = {
            "smtp_host": {},
            "smtp_port": {},
            "smtp_user": {},
            "smtp_pass": {},
            "smtp_encryption": {},
            "smtp_authentication": {},
        }
        mail_fields.update(base_fields)
        return mail_fields

    smtp_user = fields.Char(search="_search_smtp_user")
    smtp_host = fields.Char(search="_search_smtp_host")

    @api.model
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files

        Can be customized in your model
        """
        return "outgoing_mail"

    def _search_smtp_user(self, oper, value):
        servers = self.search_fetch([], ["smtp_user"]).filtered_domain(
            [("smtp_user", oper, value)]
        )
        return fields.Domain([("id", "in", servers.ids)])

    def _search_smtp_host(self, oper, value):
        servers = self.search_fetch([], ["smtp_host"]).filtered_domain(
            [("smtp_host", oper, value)]
        )
        return fields.Domain([("id", "in", servers.ids)])
