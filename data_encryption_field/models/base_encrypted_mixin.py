# Copyright 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class BaseEncryptedMixin(models.Model):

    _name = 'base.encrypted.mixin'
    _description = 'Base Encrypted Mixin'  # TODO

    name = fields.Char()
