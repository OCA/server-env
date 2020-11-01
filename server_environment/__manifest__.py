# Copyright Wingo SA
# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "server configuration environment files",
    "version": "14.0.1.0.0",
    "depends": ["base", "base_sparse_field"],
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "summary": "move some configurations out of the database",
    "website": "https://github.com/OCA/server-env",
    "license": "GPL-3 or any later version",
    "category": "Tools",
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "serv_config.xml",
    ],
    "installable": True,
}
