# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from lxml import etree

from odoo import models, api, _


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(ResConfigSettings, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)

        google_provider = self.env.ref('auth_oauth.provider_google',
                                       raise_if_not_found=False)

        if google_provider and google_provider.managed_by_env:
            readonly_fields = ['module_auth_oauth',
                               'auth_oauth_google_enabled',
                               'auth_oauth_google_client_id']
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
