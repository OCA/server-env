# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.server_environment import serv_config


SECTION = 'ir.config_parameter'


class IrConfigParameter(models.Model):

    _inherit = 'ir.config_parameter'

    is_environment = fields.Boolean(
        string="Defined by environment",
        compute="_compute_environment",
        help="If check, the value in the database will be ignored"
        " and alternatively, the system will use the key defined"
        " in your odoo.cfg environment file.")

    value = fields.Text(string="Database Value")

    environment_value = fields.Text(
        string="Environment Value",
        compute="_compute_environment",
        help="Alternative value, set in your odoo.cfg environment file.")

    @api.multi
    def _compute_environment(self):
        for parameter in self:
            parameter.is_environment = serv_config.has_option(
                SECTION, parameter.key)
            if parameter.is_environment:
                parameter.environment_value = serv_config.get(
                    SECTION, parameter.key)
            else:
                parameter.environment_value = False

    @api.model
    def get_param(self, key, default=False):
        if serv_config.has_option(SECTION, key):
            cvalue = serv_config.get(SECTION, key)
            if not cvalue:
                raise UserError(_("Key %s is empty in "
                                  "server_environment_file") %
                                (key, ))
            return cvalue
        return super().get_param(key, default=default)
