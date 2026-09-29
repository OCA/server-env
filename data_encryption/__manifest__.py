# Copyright <2019> Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Encryption data",
    "summary": "Store accounts and credentials encrypted by environment",
    "version": "18.0.1.0.1",
    "development_status": "Production/Stable",
    "maintainers": ["florian-dacosta"],
    "category": "Tools",
    "website": "https://github.com/OCA/server-env",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        # Use the same pin as Odoo to avoid compatibility issues
        "python": [
            "cryptography==3.4.8; python_version < '3.12'",
            "cryptography==42.0.8 ; python_version >= '3.12'",
        ]
    },
    "depends": ["base"],
    "data": ["security/ir.model.access.csv"],
}
