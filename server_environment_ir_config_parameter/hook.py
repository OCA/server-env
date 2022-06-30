# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def post_init_keep_parameter_value(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        env.cr.execute("""SELECT id, value FROM ir_config_parameter""")
        result = env.cr.fetchall()
        for config_id, value in result:
            env["ir.config_parameter"].browse(config_id).write({"value": value})
    return True
