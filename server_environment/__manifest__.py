# Copyright Wingo SA
# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

{
    "name": "server configuration environment files",
    "version": "13.0.3.0.0",
    "depends": ["base", "base_sparse_field"],
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "summary": "move some configurations out of the database",
    "website": "http://github.com/OCA/server-env",
    "license": "LGPL-3",
    "category": "Tools",
    "data": ["security/res_groups.xml", "serv_config.xml"],
    "installable": True,
}
