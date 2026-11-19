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

    # Reads sibling env fields (``user``, ``password``) while another one
    # (``host``) is written. Tests creating or writing a ``host`` must
    # provide a ``user`` as well.
    @api.constrains("host")
    def _check_credentials_when_host(self):
        for record in self:
            if record.host and not (record.user and record.password):
                raise ValidationError(
                    self.env._("A user and a password are required with a host.")
                )

    def _compute_password(self):
        for record in self:
            record.password = "computed_password"

    def _inverse_password(self):
        pass
