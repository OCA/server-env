# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import common
from odoo.tools import convert_file
from odoo.modules.module import get_resource_path


class TestEnv(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.ICP = self.env['ir.config_parameter']

    def _load_xml(self, module, filepath):
        convert_file(
            self.env.cr, module,
            get_resource_path(module, filepath),
            {}, mode='init', noupdate=False, kind='test')

    def test_empty(self):
        """ Empty config values cause error """
        with self.assertRaises(UserError):
            self.ICP.get_param('ircp_empty')
        self.assertEqual(self.ICP.get_param('ircp_nonexistant'), False)

    def test_regular_case(self):
        """ if a parameter is set only in the ir_config_parameter it should
        be returned"""
        self._load_xml(
            'server_environment_ir_config_parameter',
            'tests/config_param_test.xml'
        )
        value = self.ICP.get_param('ircp_from_xml')
        self.assertEqual(value, 'value_1_from_xml')

    def test_override_xmldata(self):
        """ if a parameter is in ir_config_parameter table AND
        in the odoo.cfg file, the file value should be used."""
        self._load_xml(
            'server_environment_ir_config_parameter',
            'tests/config_param_test.xml'
        )
        value = self.ICP.get_param('ircp_from_config')
        self.assertEqual(value, 'test_config_value')
