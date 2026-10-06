# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.base.models.ir_config_parameter import INVALID_VALUE
from odoo.addons.server_environment.server_env import serv_config

_logger = logging.getLogger(__name__)

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

    def _get(self, key, type_="str"):
        # all typed getters (get_str, get_int, ...) and setters read through _get
        value, id_ = super()._get(key, type_)
        if not serv_config.has_option(SECTION, key):
            return value, id_
        cvalue = serv_config.get(SECTION, key)
        if not cvalue:
            raise UserError(
                self.env._("Key %s is empty in server_environment_file", key)
            )
        if super()._get(key, "str")[0] != cvalue:
            # we write in db on first access;
            # should we have preloaded values in database at,
            # server startup, modules loading their parameters
            # from data files would break on unique key error.
            if id_:
                self.sudo().browse(id_).write({"value": cvalue})
            else:
                id_ = self.sudo().create({"key": key, "value": cvalue}).id
        try:
            return self._convert(cvalue, type_), id_
        except ValueError:
            _logger.warning(
                "server environment key %s has invalid value %r for type %s",
                key,
                cvalue,
                type_,
            )
            return INVALID_VALUE, id_

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            key = vals.get("key")
            if key and serv_config.has_option(SECTION, key):
                # enforce value from config file
                vals.update(value=serv_config.get(SECTION, key))
        return super().create(vals_list)

    def write(self, vals):
        for rec in self:
            key = vals.get("key", rec.key)
            if serv_config.has_option(SECTION, key):
                # enforce value from config file
                newvals = dict(vals, value=serv_config.get(SECTION, key))
            else:
                newvals = vals
            super(IrConfigParameter, rec).write(newvals)
        return True
