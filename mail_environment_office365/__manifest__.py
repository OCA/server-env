# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Anna Janiszewska <anna.janiszewska@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Server environment configuration for Office365",
    "summary": """ Configure Office365 parameters with environment variables
    via server_environment""",
    "version": "13.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-env",
    "license": "AGPL-3",
    "category": "Tools",
    "depends": [
        "microsoft_outlook",
        "server_environment",
        "server_environment_ir_config_parameter",
    ],
}
