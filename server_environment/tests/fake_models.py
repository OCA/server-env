# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models

# pylint: disable=consider-merging-classes-inherited


class FakePartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "server.env.mixin"]

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        partner_fields = {
            "city": {},
        }
        partner_fields.update(base_fields)
        return partner_fields

    @api.model
    def _server_env_global_section_name(self):
        return "partner"
