# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError

from odoo.addons.server_environment.server_env import serv_config

SECTION = "ir.config_parameter"


class IrConfigParameter(models.Model):
    _name = "ir.config_parameter"
    _inherit = ["ir.config_parameter", "server.env.mixin"]

    _server_env_section_name_field = "key"

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        parameter_fields = {
            "value": {},
        }
        parameter_fields.update(base_fields)
        return parameter_fields

    @api.model
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files

        Can be customized in your model
        """
        return SECTION

    @api.model
    def get_param(self, key, default=False):
        value = super().get_param(key, default=None)
        section = "%s.%s" % (SECTION, key)
        if serv_config.has_option(section, "value"):
            cvalue = serv_config.get(section, "value")
            if not cvalue:
                raise UserError(
                    _("Key %s is empty in " "server_environment_file") % (key,)
                )
            if cvalue != value:
                # we write in db on first access;
                # should we have preloaded values in database at,
                # server startup, modules loading their parameters
                # from data files would break on unique key error.
                self.sudo().set_param(key, cvalue)
                value = cvalue
        if value is None:
            return default
        return value

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # in case of creation of a param which is in config file but with another value
        # the value is in cache after creation and then a get_param will give back the
        # cache value instead of reading the field from the config...
        # so if there is a config value, we clean the cache so it will be taken into
        # account of the next read
        if record._server_env_has_key_defined("value"):
            record.invalidate_cache(fnames=["value"], ids=record.ids)
        return record

    def write(self, vals):
        res = super().write(vals)
        # in case of creation of a param which is in config file but with another value
        # the value is in cache after creation and then a get_param will give back the
        # cache value instead of reading the field from the config...
        # so if there is a config value, we clean the cache so it will be taken into
        # account of the next read
        for record in self:
            if record._server_env_has_key_defined("value"):
                record.invalidate_cache(fnames=["value"], ids=record.ids)
        return res
