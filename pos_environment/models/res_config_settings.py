# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    receipt_environment_header = fields.Text(
        related="pos_config_id.receipt_environment_header"
    )

    receipt_environment_footer = fields.Text(
        related="pos_config_id.receipt_environment_footer"
    )
