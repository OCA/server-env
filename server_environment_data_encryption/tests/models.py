# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models
from odoo.exceptions import ValidationError

# pylint: disable=consider-merging-classes-inherited


class FakePartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "server.env.mixin"]

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        partner_fields = {
            "city": {},
            "street": {},
            "street2": {},
        }
        partner_fields.update(base_fields)
        return partner_fields

    @api.model
    def _server_env_global_section_name(self):
        return "partner"

    @api.constrains("street")
    def _check_street2_when_street(self):
        """A constraint reading a sibling env field (``street2``) while another
        env field (``street``) is written. It must see the current value of
        ``street2``, not a stale one."""
        for partner in self.filtered(lambda p: p.street):
            if not partner.street2:
                raise ValidationError(
                    self.env._("Street2 is required when Street is set.")
                )
