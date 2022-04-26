# Copyright 2021 Camptocamp SA (http://www.camptocamp.ch)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Auth SAML environment",
    "summary": "Configure SAML authentication providers through environment variables",
    "version": "14.0.1.0.1",
    "category": "base",
    "author": "Camptocamp SA,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-env",
    "license": "AGPL-3",
    "depends": [
        "auth_saml",
        "server_environment",
    ],
    "data": [
        "views/saml_provider_view.xml",
    ],
    "installable": True,
}
