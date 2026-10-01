from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ExternalService(models.Model):
    _name = "external.service"
    _description = "External Service"
    _inherit = "server.env.mixin"

    name = fields.Char(required=True, help="Name of the service")
    description = fields.Char(required=True, help="Description of the service")
    host = fields.Char(help="Host of the service")
    user = fields.Char(help="User to connect to the service")
    password = fields.Char(help="Password to connect to the service")

    @api.model
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files

        Can be customized in your model
        """
        return "external_service"

    @property
    def _server_env_fields(self):
        return {
            "host": {},
            "user": {},
            "password": {
                "no_default_field": True,
                "compute_default": "_compute_password",
                "inverse_default": "_inverse_password",
            },
        }

    @api.constrains("host")
    def _check_user_when_host(self):
        """Read a sibling env field (``user``) while another one (``host``)
        is written."""
        for record in self:
            if record.host and not record.user:
                raise ValidationError(self.env._("A user is required with a host."))

    def _compute_password(self):
        for record in self:
            record.password = "computed_password"

    def _inverse_password(self):
        pass
