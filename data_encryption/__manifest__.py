# Copyright <2019> Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Encryption data",
    "summary": "Store accounts and credentials encrypted by environment",
    "version": "14.0.1.0.0",
    "development_status": "Alpha",
    "category": "Tools",
    "website": "https://github.com/OCA/server-env",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": ["cryptography"]},
    "depends": ["base"],
    "data": ["security/ir.model.access.csv"],
}
