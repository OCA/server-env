# Copyright Wingo SA
# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

{
    "name": "server configuration environment files",
    "version": "18.0.1.0.0",
    "depends": ["base", "base_sparse_field"],
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "summary": "move some configurations out of the database",
    "website": "https://github.com/OCA/server-env",
    "license": "LGPL-3",
    "development_status": "Production/Stable",
    "category": "Tools",
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "serv_config.xml",
    ],
    "installable": True,
}
