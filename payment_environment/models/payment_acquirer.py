# Copyright 2021 Camptocamp SA
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import models


class PaymentAcquirer(models.Model):
    _name = "payment.acquirer"
    _inherit = [
        "payment.acquirer",
        "server.env.techname.mixin",
        "server.env.mixin",
    ]

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        acquirer_fields = {
            "state": {},
        }
        acquirer_fields.update(base_fields)
        return acquirer_fields
