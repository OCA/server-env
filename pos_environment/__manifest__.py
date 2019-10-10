# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Point of Sale - Custom Bill by Environment',
    'summary': "Custom messages on the bill depending on the environment",
    'version': '12.0.1.0.0',
    'category': 'Point of Sale',
    'author': 'GRAP,Odoo Community Association (OCA)',
    'website': 'https://github.com/oca/server-env',
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
    'installable': True,
}
