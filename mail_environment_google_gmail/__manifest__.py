# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mail configuration with server_environment for Google Gmail",
    "summary": "Configure Gmail mail servers with server_environment_files",
    "version": "19.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["ivantodorovich"],
    "website": "https://github.com/OCA/server-env",
    "license": "AGPL-3",
    "category": "Tools",
    "depends": [
        "google_gmail",
        "mail_environment",
        "server_environment_ir_config_parameter",
    ],
}
