# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.server_environment.server_env import serv_config

SECTION = "ir.config_parameter"


class IrConfigParameter(models.Model):

    _inherit = "ir.config_parameter"

    is_environment = fields.Boolean(
        string="Defined by environment",
        compute="_compute_is_environment",
        help="If check, the value in the database will be ignored"
        " and alternatively, the system will use the key defined"
        " in your odoo.cfg environment file.",
    )

    def _compute_is_environment(self):
        for parameter in self:
            parameter.is_environment = serv_config.has_option(SECTION, parameter.key)

    @api.model
    def get_param(self, key, default=False):
        value = super().get_param(key, default=None)
        if serv_config.has_option(SECTION, key):
            allow_empty = self.env.context.get("icp_get_param__allow_empty")
            cvalue = serv_config.get(SECTION, key)
            if not cvalue and not allow_empty:
                raise UserError(
                    _("Key %s is empty in " "server_environment_file") % (key,)
                )
            if cvalue != value:
                # we write in db on first access;
                # should we have preloaded values in database at,
                # server startup, modules loading their parameters
                # from data files would break on unique key error.
                if not self.env.context.get("_from_get_param", 0):
                    # the check is to avoid recursion, for instance the mail
                    # addon has an override in ir.config_parameter::write which
                    # calls get_param if we are setting mail.catchall.alias and
                    # this will cause an infinite recursion. We cut that
                    # recursion by using the context check.
                    #
                    # The mail addon call to get_param expects to get the value
                    # *before* the change, so we have to return the database
                    # value in that case
                    self.sudo().with_context(_from_get_param=1).set_param(key, cvalue)
                    value = cvalue
        if value is None:
            return default
        return value

    @api.model
    def create(self, vals):
        key = vals.get("key")
        if serv_config.has_option(SECTION, key):
            # enforce value from config file
            vals = dict(vals, value=serv_config.get(SECTION, key))
        return super().create(vals)

    def write(self, vals):
        for rec in self:
            key = vals.get("key") or rec.key
            if serv_config.has_option(SECTION, key):
                # enforce value from config file
                newvals = dict(vals, value=serv_config.get(SECTION, key))
            else:
                newvals = vals
            super().write(newvals)
        return True
