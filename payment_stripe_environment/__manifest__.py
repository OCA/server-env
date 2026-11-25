# Copyright 2026 Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Payment Stripe Environment",
    "summary": "Configure Stripe with server environment",
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Accounting/Payment Providers",
    "website": "https://github.com/OCA/server-env",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["hparfr"],
    "license": "AGPL-3",
    "depends": [
        "payment_stripe",
        "server_environment",
    ],
    "data": [],
    "demo": [],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
