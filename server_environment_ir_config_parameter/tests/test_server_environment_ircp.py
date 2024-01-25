# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from os import path

from odoo.exceptions import UserError
from odoo.tools import convert_file, file_path

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

from ..models import ir_config_parameter

CONFIG = """
    [ir.config_parameter]
    ircp_from_config=config_value
    other_ircp_from_config=other_config_value
    ircp_without_record=config_value_without_record
    other_ircp_without_record=other_config_value_without_record
    ircp_empty=
    mail.catchall.alias=my_alias
"""


class TestEnv(ServerEnvironmentCase):
    def setUp(self):
        super().setUp()
        self.ICP = self.env["ir.config_parameter"]
        self.env_config = CONFIG

    def _load_xml(self, module, filepath):
        convert_file(
            self.env,
            module,
            path.join(file_path(module), filepath),
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
        ):
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

    def test_read_mail_catchall_alias(self):
        """read mail.catchall.alias from server env:

        this must not break the mail addon's overload"""
        with self.load_config(
            public=self.env_config, serv_config_class=ir_config_parameter
        ):
            value = self.ICP.get_param("mail.catchall.alias")
            self.assertEqual(value, "my_alias")
            res = self.ICP.search([("key", "=", "mail.catchall.alias")])
            self.assertEqual(len(res), 1)
            self.assertEqual(res.value, "my_alias")

    def test_write(self):
        # there's a write override, test it here
        self._load_xml(
            "server_environment_ir_config_parameter", "tests/config_param_test.xml"
        )
        with self.load_config(
            public=self.env_config, serv_config_class=ir_config_parameter
        ):
            ICP = self.ICP
            icp1 = ICP.search([("key", "=", "ircp_from_config")])
            self.assertEqual(icp1.value, "value_from_xml")
            icp2 = ICP.search([("key", "=", "other_ircp_from_config")])
            self.assertEqual(icp2.value, "other_value_from_xml")
            # Ensures that each record has its own value at write
            (icp1 | icp2).write({"value": "test"})
            self.assertEqual(icp1.value, "config_value")
            self.assertEqual(icp2.value, "other_config_value")
            self.assertEqual(ICP.get_param(icp1.key), "config_value")
            self.assertEqual(ICP.get_param(icp2.key), "other_config_value")

    def test_create(self):
        self._load_xml(
            "server_environment_ir_config_parameter", "tests/config_param_test.xml"
        )
        with self.load_config(
            public=self.env_config, serv_config_class=ir_config_parameter
        ):
            vals = [
                {
                    "key": "ircp_without_record",
                    "value": "NOPE",
                },
                {
                    "key": "other_ircp_without_record",
                    "value": "NOPE",
                },
            ]
            records = self.ICP.create(vals)
            # Ensures each record has its own value at create
            self.assertEqual(
                records.mapped("value"),
                ["config_value_without_record", "other_config_value_without_record"],
            )
