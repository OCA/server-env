# Copyright 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _inverse_private_text(self):
        field_names = ["private_text"]
        EncryptedData = self.env["encrypted.data"].sudo()
        for record in self:
            encrypted_data_name = "fields:%s,%s" % (
                record._name, record.id)
            # values = EncryptedData._encrypted_read_json(
            #     encrypted_data_name, env=env)
            values = {x: getattr(record, x) for x in field_names}
            EncryptedData._encrypted_store_json(
                encrypted_data_name, values
            )

    def _compute_private_text(self):
        EncryptedData = self.env["encrypted.data"].sudo()
        for record in self:
            field_names = ["private_text"]
            encrypted_data_name = "fields:%s,%s" % (
                record._name, record.id)
            stored_values = EncryptedData._encrypted_read_json(
                encrypted_data_name)
            values = {x: stored_values.get(x) for x in field_names}
            for field in field_names:
                setattr(record, field, values.get(field))

    private_text = fields.Text(
        compute="_compute_private_text",
        inverse="_inverse_private_text",
    )
