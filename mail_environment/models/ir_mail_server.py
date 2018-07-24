# Copyright 2012-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class IrMailServer(models.Model):
    _name = "ir.mail_server"
    _inherit = ["ir.mail_server", "server.env.mixin"]

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        mail_fields = {
            "smtp_host": {},
            "smtp_port": {},
            "smtp_user": {},
            "smtp_pass": {},
            "smtp_encryption": {},
        }
        mail_fields.update(base_fields)
        return mail_fields

    @api.model
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files

        Can be customized in your model
        """
        return 'outgoing_mail'
