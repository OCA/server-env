# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.server_environment.server_env import serv_config

SECTION = "ir.config_parameter"


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    is_environment = fields.Boolean(
        string="Defined by environment",
        compute="_compute_is_environment",
        help="If check, the value in the database will be ignored"
        " and alternatively, the system will use the key defined"
        " in your odoo.cfg environment file.",
    )

    def _compute_is_environment(self):
        for parameter in self:
            parameter.is_environment = serv_config.has_option(SECTION, parameter.key)

    @api.model
    def get_param(self, key, default=False):
        value = super().get_param(key, default=None)
        if serv_config.has_option(SECTION, key):
            cvalue = serv_config.get(SECTION, key)
            if not cvalue:
                raise UserError(
                    _("Key %s is empty in " "server_environment_file") % (key,)
                )
            if cvalue != value:
                value = cvalue
        if value is None:
            return default
        return value

    def read(self, _fields=None, load="_classic_read"):
        res = super().read(_fields, load=load)
        environment_values = [r for r in res if r["is_environment"]]
        for environment_value in environment_values:
            environment_value["value"] = serv_config.get(
                SECTION, environment_value["key"]
            )
        return res
