# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.addons.server_environment import serv_config


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Columns section
    receipt_environment_header = fields.Text(
        string='Receipt Environment Header',
        compute='_compute_receipt_environment_header')

    receipt_environment_footer = fields.Text(
        string='Receipt Environment Footer',
        compute='_compute_receipt_environment_footer')

    @api.multi
    def _compute_receipt_environment_header(self):
        for config in self:
            config.receipt_environment_header =\
                self._get_receipt_environment_part('header')

    @api.multi
    def _compute_receipt_environment_footer(self):
        for config in self:
            config.receipt_environment_footer =\
                self._get_receipt_environment_part('footer')

    @api.model
    def _get_receipt_environment_part(self, part):
        section_name = 'pos_environment_%s' % part
        line_list = []
        if serv_config.has_section(section_name):
            # Parse each line
            for item in serv_config.items(section_name):
                if '__' not in item[0]:
                    # Universal line
                    line_list.append(item[1])
                elif '__%s' % (self.env.user.lang) in item[0]:
                    # depend of the language
                    line_list.append(item[1])
        return '\n'.join(line_list)
