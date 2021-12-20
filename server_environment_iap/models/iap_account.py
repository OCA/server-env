# Copyright 2021 Camptocamp SA <https://www.camptocamp.com/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.server_environment.server_env import serv_config

SECTION = "iap.account"


class IapAccount(models.Model):

    _inherit = "iap.account"

    is_environment = fields.Boolean(
        string="Defined by environment",
        compute="_compute_is_environment",
        help="If check, the value in the database will be ignored"
        " and alternatively, the system will use the service name defined"
        " in your odoo.cfg environment file.",
    )

    def _compute_is_environment(self):
        for account in self:
            account.is_environment = serv_config.has_option(
                SECTION, account.service_name
            )

    @api.model
    def get(self, service_name, force_create=True):
        account = super().get(service_name, force_create=True)
        if serv_config.has_option(SECTION, service_name):
            cvalue = serv_config.get(SECTION, service_name)
            if not cvalue:
                # if service name is empty it's probably not a production instance,
                # so we need to remove it from database
                account.unlink()
                raise UserError(
                    _("Service name %s is empty in " "server_environment_file")
                    % (service_name,)
                )
            if cvalue != account.account_token:
                # we write in db on first access;
                # should we have preloaded values in database at,
                # server startup, modules loading their parameters
                # from data files would break on unique key error.
                account.account_token = cvalue
        return account

    @api.model
    def create(self, vals):
        service_name = vals.get("service_name")
        if serv_config.has_option(SECTION, service_name):
            # enforce account_token from config file
            vals = dict(vals, account_token=serv_config.get(SECTION, service_name))
        return super().create(vals)

    def write(self, vals):
        for rec in self:
            service_name = vals.get("service_name") or rec.service_name
            if serv_config.has_option(SECTION, service_name):
                # enforce account_token from config file
                newvals = dict(
                    vals, account_token=serv_config.get(SECTION, service_name)
                )
            else:
                newvals = vals
            super().write(newvals)
        return True
