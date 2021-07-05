# Copyright 2020 Camptocamp (http://www.camptocamp.com)
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.http_routing.models.ir_http import slugify


class ServerEnvTechNameMixin(models.AbstractModel):
    """Provides a tech_name field to be used in server env vars as unique key.

    The `name` field can be error prone because users can easily change it
    to something more meaningful for them or set weird chars into it
    that make difficult to reference the record in env var config.
    This mixin helps solve the problem by providing a tech name field
    and a cleanup machinery as well as a unique constrain.

    Use it in place of "server.env.mixin".
    """

    _name = "server.env.techname.mixin"
    _inherit = "server.env.mixin"
    _description = "Server environment technical name"
    _sql_constraints = [
        ("tech_name_uniq", "unique(tech_name)", "`tech_name` must be unique!",)
    ]

    tech_name = fields.Char(
        string="Environment Technical Name",
        help="Unique name for server environment configuration keys.",
        compute="_compute_tech_name",
        store=True,
        readonly=False,
    )

    _server_env_section_name_field = "tech_name"

    @api.depends("name")
    def _compute_tech_name(self):
        for rec in self:
            # Update tech_name only if it hasn't been set or if we're
            # dealing with a new record.
            if not rec.tech_name or not rec._origin.id:
                rec.tech_name = self._normalize_tech_name(rec.name)

    @api.onchange("tech_name")
    def _onchange_tech_name(self):
        # make sure it's normalized
        res = {}
        normalized = self._normalize_tech_name(self.tech_name)
        if self.tech_name != normalized:
            res = {
                "warning": {
                    "title": _("Technical Name"),
                    "message": _(
                        "Environment Technical Name '%s' can't "
                        "contain special characters."
                    )
                    % self.tech_name,
                }
            }
            self.tech_name = normalized
        return res

    @api.constrains("tech_name")
    def _check_tech_name(self):
        for rec in self.filtered("tech_name"):
            if rec.tech_name != self._normalize_tech_name(rec.tech_name):
                raise ValidationError(
                    _(
                        "Environment Technical Name '%s' can't "
                        "contain special characters."
                    )
                    % rec.tech_name
                )

    @staticmethod
    def _normalize_tech_name(name):
        if not name:
            return name
        return slugify(name).replace("-", "_")
