# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
from lxml import etree

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
                value = res.get(option)
                conf_value = serv_config.get(SECTION, option)
                if not conf_value:
                    raise UserError(
                        _('Option %s is empty in server_environment_file')
                        % option)
                if conf_value != value:
                    res[option] = conf_value
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(ResConfigSettings, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if serv_config.has_section(SECTION):
            doc = etree.XML(res['arch'])
            for option in serv_config.options(SECTION):
                for node in doc.xpath("//field[@name='%s']" % option):
                    node.set('readonly', '1')
                    modifiers = json.loads(node.get("modifiers"))
                    modifiers['readonly'] = True
                    node.set("modifiers", json.dumps(modifiers))

                    node.set('help', _('This field is managed through server '
                                       'environment'))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
