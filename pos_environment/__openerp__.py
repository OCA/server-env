# coding: utf-8
# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Point of Sale - Custom Bill by Environment',
    'summary': "Custom messages on the bill depending on the environment",
    'version': '8.0.1.0.0',
    'category': 'Point of Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'server_environment',
    ],
    'data': [
        'views/templates.xml',
        'views/view_pos_config.xml',
    ],
    'qweb': [
        'static/src/xml/pos_environment.xml',
    ],
    'images': [
    ],
    'installable': False,
}
