# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Server Environment Ir Config Parameter",
    "summary": """
        Override System Parameters from server environment file""",
    "version": "14.0.1.1.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-env",
    "depends": ["server_environment"],
    "post_init_hook": "post_init_keep_parameter_value",
    "data": [],
}
