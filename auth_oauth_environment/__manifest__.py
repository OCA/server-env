# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Auth oauth configuration with server_environment",
    "version": "17.0.1.0.0",
    "category": "Tools",
    "summary": "Configure OAuth providers with server_environment_files",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/server-env",
    "depends": [
        "auth_oauth",
        "server_environment",
    ],
    "data": [
        "data/auth_oauth_provider.xml",
        "views/auth_oauth_provider_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "auto_install": False,
    "installable": True,
}
