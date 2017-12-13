# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from lxml import etree

from odoo import fields, models, api, _
from odoo.addons.server_environment import serv_config


class AuthOAuthProvider(models.Model):

    _inherit = 'auth.oauth.provider'

    managed_by_env = fields.Boolean(compute='_compute_server_env')
    provider_simple_name = fields.Char(compute='_compute_simple_name')
    client_id = fields.Char(string='Client ID', compute='_compute_server_env')
    enabled = fields.Boolean(string='Allowed', compute='_compute_server_env',
                             search='_search_enabled')

    def _compute_server_env(self):
        for provider in self:
            provider_section_name = provider._get_provider_section_name()
            vals = {}

            if serv_config.has_section(provider_section_name):

                vals.update({'managed_by_env': True})
                vals.update(serv_config.items(provider_section_name))
            else:
                vals.update({'managed_by_env': False, 'enabled': False})
            provider.update(vals)

    def _search_enabled(self, operator, value):
        enabled_provider_ids = []
        for provider in self.search([]):
            provider_section_name = provider._get_provider_section_name()
            if serv_config.has_option(provider_section_name, 'enabled') \
                    and serv_config.get(provider_section_name, 'enabled'):
                enabled_provider_ids.append(provider.id)
        return [('id', 'in', enabled_provider_ids)]

    @api.multi
    def _compute_simple_name(self):
        for provider in self:
            provider.provider_simple_name = provider.name.split(' ')[0].lower()

    @api.one
    def _get_provider_section_name(self):
        return '.'.join(['auth_oauth', self.provider_simple_name])

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(AuthOAuthProvider, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        readonly_fields = ['enabled', 'client_id']
        doc = etree.XML(res['arch'])
        for ro_field in readonly_fields:
            for node in doc.xpath("//field[@name='%s']" % ro_field):
                node.set('readonly', '1')
                modifiers = json.loads(node.get("modifiers"))
                modifiers['readonly'] = True
                node.set("modifiers", json.dumps(modifiers))

                node.set('help', _('This field is managed through server '
                                   'environment'))
        res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
