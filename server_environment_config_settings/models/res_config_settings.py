# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, _
from odoo.exceptions import UserError
from odoo.addons.server_environment import serv_config


SECTION = 'res.config.settings'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        if serv_config.has_section(SECTION):
            for option in serv_config.options(SECTION):
                import pdb; pdb.set_trace()
                value = res.get(option)
                conf_value = serv_config.get(SECTION, option)
                if not conf_value:
                    raise UserError(
                        _('Option %s is empty in server_environment_file')
                        % option)
                if conf_value != value:
                    res[option] = conf_value
        return res
