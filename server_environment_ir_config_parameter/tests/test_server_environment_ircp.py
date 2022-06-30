# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.modules.module import get_resource_path
from odoo.tools import convert_file

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

from ..models import ir_config_parameter


class TestEnv(ServerEnvironmentCase):
    def setUp(self):
        super().setUp()
        self.ICP = self.env["ir.config_parameter"]
        self.env_config = (
            "[ir.config_parameter.ircp_from_config]\n"
            "value=config_value\n\n"
            "[ir.config_parameter.ircp_empty]\n"
            "value=\n\n"
        )

    def _load_xml(self, module, filepath):
        convert_file(
            self.env.cr,
            module,
            get_resource_path(module, filepath),
            {},
            mode="init",
            noupdate=False,
            kind="test",
        )

    def test_get_param(self):
        """Get system parameter from config"""
        with self.load_config(
            public=self.env_config, serv_config_class=ir_config_parameter
        ):
            # it's not in db
            res = self.ICP.search([("key", "=", "ircp_from_config")])
            self.assertFalse(res)
            # read so it's created in db
            value = self.ICP.get_param("ircp_from_config")
            self.assertEqual(value, "config_value")
            # now it's in db
            res = self.ICP.search([("key", "=", "ircp_from_config")])
            self.assertEqual(len(res), 1)
            self.assertEqual(res.value, "config_value")

    def test_set_param_1(self):
        """We can't set parameters that are in config file"""
        with self.load_config(
            public=self.env_config, serv_config_class=ir_config_parameter
        ), self.load_config(public=self.env_config):
            # when creating, the value is overridden by config file
            self.ICP.set_param("ircp_from_config", "new_value")
            value = self.ICP.get_param("ircp_from_config")
            self.assertEqual(value, "config_value")
            # when writing, the value is overridden by config file
            res = self.ICP.search([("key", "=", "ircp_from_config")])
            self.assertEqual(len(res), 1)
            res.write({"value": "new_value"})
            value = self.ICP.get_param("ircp_from_config")
            self.assertEqual(value, "config_value")
            # unlink works normally...
            res = self.ICP.search([("key", "=", "ircp_from_config")])
            self.assertEqual(len(res), 1)
            res.unlink()
            res = self.ICP.search([("key", "=", "ircp_from_config")])
            self.assertEqual(len(res), 0)
            # but the value is recreated when getting param again
            value = self.ICP.get_param("ircp_from_config")
            self.assertEqual(value, "config_value")
            res = self.ICP.search([("key", "=", "ircp_from_config")])
            self.assertEqual(len(res), 1)

    def test_set_param_2(self):
        """We can set parameters that are not in config file"""
        with self.load_config(
            public=self.env_config, serv_config_class=ir_config_parameter
        ):
            self.ICP.set_param("some.param", "new_value")
            self.assertEqual(self.ICP.get_param("some.param"), "new_value")
            res = self.ICP.search([("key", "=", "some.param")])
            res.unlink()
            res = self.ICP.search([("key", "=", "some.param")])
            self.assertFalse(res)

    def test_empty(self):
        """Empty config values cause error"""
        with self.load_config(
            public=self.env_config, serv_config_class=ir_config_parameter
        ):
            with self.assertRaises(UserError):
                self.ICP.get_param("ircp_empty")
            self.assertEqual(self.ICP.get_param("ircp_nonexistant"), False)

    def test_override_xmldata(self):
        with self.load_config(
            public=self.env_config, serv_config_class=ir_config_parameter
        ):
            self._load_xml(
                "server_environment_ir_config_parameter", "tests/config_param_test.xml"
            )
            value = self.ICP.get_param("ircp_from_config")
            self.assertEqual(value, "config_value")
