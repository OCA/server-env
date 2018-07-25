# Copyright 2012-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import operator
from odoo import api, fields, models


class FetchmailServer(models.Model):
    """Incoming POP/IMAP mail server account"""
    _name = 'fetchmail.server'
    _inherit = ["fetchmail.server", "server.env.mixin"]

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        mail_fields = {
            "server": {},
            "port": {},
            "type": {},
            "user": {},
            "password": {},
            "is_ssl": {},
            "attach": {},
            "original": {},
        }
        mail_fields.update(base_fields)
        return mail_fields

    type = fields.Selection(search='_search_type')

    @api.model
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files

        Can be customized in your model
        """
        return 'incoming_mail'

    @api.model
    def _search_type(self, oper, value):
        operators = {
            '=': operator.eq,
            '!=': operator.ne,
            'in': operator.contains,
            'not in': lambda a, b: not operator.contains(a, b),
        }
        if oper not in operators:
            return [('id', 'in', [])]
        servers = self.search([]).filtered(
            lambda s: operators[oper](value, s.type)
        )
        return [('id', 'in', servers.ids)]
