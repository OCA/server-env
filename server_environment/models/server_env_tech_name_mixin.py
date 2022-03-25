# Copyright 2020 Camptocamp (http://www.camptocamp.com)
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.addons.http_routing.models.ir_http import slugify


class ServerEnvTechNameMixin(models.AbstractModel):
    """Provides a tech_name field to be used in server env vars as unique key.

    The `name` field can be error prone because users can easily change it
    to something more meaningful for them or set weird chars into it
    that make difficult to reference the record in env var config.
    This mixin helps solve the problem by providing a tech name field
    and a cleanup machinery as well as a unique constrain.

    To use this mixin add it to the _inherit attr of your module like:

        _inherit = [
            "my.model",
            "server.env.techname.mixin",
            "server.env.mixin",
        ]

    """

    _name = "server.env.techname.mixin"
    _description = "Server environment technical name"
    # TODO: could leverage the new option for computable / writable fields
    # and get rid of some onchange / read / write code.
    tech_name = fields.Char(
        help="Unique name for technical purposes. Eg: server env keys.",
    )

    _server_env_section_name_field = "tech_name"
    _tech_name_unique_per_company = False   # off by default

    @api.constrains("tech_name", "company_id")
    def _check_tech_name(self):
        company_dependent = self._tech_name_unique_per_company and  "company_id" in self._fields
        for record in self:
            domain = [('id', '!=', record.id), ('tech_name', '=' , record.tech_name)]
            error_msg = _("Tech name %s is duplicated. Tech name must be unique") % record.tech_name
            if company_dependent:
                domain.append(('company_id', '=', record.company_id.id))
                error_msg += _(" per company")
            if self.search_count(domain):
                raise ValidationError(error_msg)
                
    @api.onchange("name")
    def _onchange_name_for_tech(self):
        # Keep this specific name for the method to avoid possible overrides
        # of existing `_onchange_name` methods
        if self.name and not self.tech_name:
            self.tech_name = self.name

    @api.onchange("tech_name")
    def _onchange_tech_name(self):
        if self.tech_name:
            # make sure is normalized
            self.tech_name = self._normalize_tech_name(self.tech_name)

    @api.model
    def create(self, vals):
        self._handle_tech_name(vals)
        return super().create(vals)

    def write(self, vals):
        self._handle_tech_name(vals)
        return super().write(vals)

    def _handle_tech_name(self, vals):
        # make sure technical names are always there
        if not vals.get("tech_name") and vals.get("name"):
            vals["tech_name"] = self._normalize_tech_name(vals["name"])

    @staticmethod
    def _normalize_tech_name(name):
        return slugify(name).replace("-", "_")
