# Copyright 2012-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class FetchmailServer(models.Model):
    """Incoming POP/IMAP mail server account"""

    _name = "fetchmail.server"
    _inherit = ["fetchmail.server", "server.env.mixin"]  # noqa: RUF012

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        mail_fields = {
            "server": {},
            "port": {},
            "server_type": {},
            "user": {},
            "password": {},
            "is_ssl": {},
            "attach": {},
            "original": {},
        }
        mail_fields.update(base_fields)
        return mail_fields

    is_ssl = fields.Boolean(search="_search_is_ssl")
    server_type = fields.Selection(search="_search_server_type")

    @api.model
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files

        Can be customized in your model
        """
        return "incoming_mail"

    def _search_is_ssl(self, oper, value):
        servers = self.search_fetch([], ["is_ssl"]).filtered_domain(
            [("is_ssl", oper, value)]
        )
        return fields.Domain([("id", "in", servers.ids)])

    def _search_server_type(self, oper, value):
        servers = self.search_fetch([], ["server_type"]).filtered_domain(
            [("server_type", oper, value)]
        )
        return [("id", "in", servers.ids)]
