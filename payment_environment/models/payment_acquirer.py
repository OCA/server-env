# Copyright 2021 Camptocamp SA
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models
from odoo.osv import expression


class PaymentAcquirer(models.Model):
    _name = "payment.acquirer"
    _inherit = [
        "payment.acquirer",
        "server.env.techname.mixin",
        "server.env.mixin",
    ]
    _order = "module_state, sequence, name"

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        acquirer_fields = {
            "state": {},
        }
        acquirer_fields.update(base_fields)
        return acquirer_fields

    state = fields.Selection(
        search="_search_state",
    )

    def _search_state(self, operator, value):
        """
        As state field is now managed as server environment fields,
        the field is considered as a computed fields.
        Then, we need to define a custom search function
        to be able to search on this field.

        We don't want to cover all cases,
        just search implemented in core function
        to display the acquirers when generating the payment link.

        See module payment in controller/portal.py function pay()

        Used domain is: ('state', 'in', ['enabled', 'test'])
        """
        if operator == "in" and isinstance(value, list):
            valid_acquirers = self.search([]).filtered_domain([("state", "in", value)])
            if valid_acquirers:
                return [("id", "in", valid_acquirers.ids)]

        return expression.FALSE_DOMAIN
