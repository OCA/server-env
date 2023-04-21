# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Point of Sale - Custom Bill by Environment",
    "summary": "Custom messages on the bill depending on the environment",
    "version": "16.0.1.0.1",
    "category": "Point of Sale",
    "author": "GRAP,Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/server-env",
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
        "server_environment",
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_environment/static/src/xml/ReceiptScreen.xml",
        ],
    },
    "installable": True,
}
