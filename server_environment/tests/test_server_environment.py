# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
import os
from unittest.mock import patch

from odoo.tools.config import config as odoo_config

from .. import server_env
from . import common


class TestEnv(common.ServerEnvironmentCase):
    def test_view(self):
        model = self.env["server.config"]
        view = model.fields_view_get()
        self.assertTrue(view)

    def _test_default(self, hidden_pwd=False):
        model = self.env["server.config"]
        rec = model.create({})
        defaults = rec.default_get([])
        self.assertTrue(defaults)
        self.assertIsInstance(defaults, dict)
        pass_checked = False
        for default in defaults:
            if "passw" in default:
                check = self.assertEqual if hidden_pwd else self.assertNotEqual
                check(defaults[default], "**********")
                pass_checked = True
        self.assertTrue(pass_checked)

    @patch.dict(odoo_config.options, {"running_env": "dev"})
    def test_default_dev(self):
        self._test_default()

    @patch.dict(odoo_config.options, {"running_env": "whatever"})
    def test_default_non_dev_env(self):
        server_env._load_running_env()
        self._test_default(hidden_pwd=True)

    @patch.dict(odoo_config.options, {"running_env": None})
    @patch.dict(os.environ, {"RUNNING_ENV": "dev"})
    def test_default_dev_from_environ(self):
        server_env._load_running_env()
        self._test_default()

    @patch.dict(odoo_config.options, {"running_env": None})
    @patch.dict(os.environ, {"ODOO_STAGE": "dev"})
    def test_odoosh_dev_from_environ(self):
        server_env._load_running_env()
        self._test_default()

    @patch.dict(odoo_config.options, {"running_env": "testing"})
    def test_value_retrival(self):
        with self.set_config_dir("testfiles"):
            parser = server_env._load_config()
            val = parser.get("external_service.ftp", "user")
            self.assertEqual(val, "testing")
            val = parser.get("external_service.ftp", "host")
            self.assertEqual(val, "sftp.example.com")

    @patch.dict(os.environ, {"SERVER_ENVIRONMENT_ALLOW_OVERWRITE_OPTIONS_SECTION": "0"})
    @patch.dict(
        odoo_config.options,
        {
            "running_env": "testing",
            "server_environment_allow_overwrite_options_section": True,
            "odoo_test_option": "fake odoo config",
        },
    )
    def test_server_environment_allow_overwrite_options_section(self):
        with self.set_config_dir("testfiles"):
            server_env._load_config()
            self.assertEqual(
                odoo_config["odoo_test_option"], "Set in config file for testing env"
            )

    @patch.dict(os.environ, {"SERVER_ENVIRONMENT_ALLOW_OVERWRITE_OPTIONS_SECTION": "1"})
    @patch.dict(
        odoo_config.options,
        {
            "running_env": "testing",
            "server_environment_allow_overwrite_options_section": False,
            "odoo_test_option": "fake odoo config",
        },
    )
    def test_server_environment_disabled_overwrite_options_section(self):
        with self.set_config_dir("testfiles"):
            server_env._load_config()
            self.assertEqual(odoo_config["odoo_test_option"], "fake odoo config")

    @patch.dict(os.environ, {"SERVER_ENVIRONMENT_ALLOW_OVERWRITE_OPTIONS_SECTION": "1"})
    @patch.dict(
        odoo_config.options,
        {
            "running_env": "testing",
            "odoo_test_option": "fake odoo config",
        },
    )
    def test_server_environment_allow_overwrite_options_section_by_env(self):
        with self.set_config_dir("testfiles"):
            server_env._load_config()
            self.assertEqual(
                odoo_config["odoo_test_option"], "Set in config file for testing env"
            )

    @patch.dict(os.environ, {"SERVER_ENVIRONMENT_ALLOW_OVERWRITE_OPTIONS_SECTION": "0"})
    @patch.dict(
        odoo_config.options,
        {
            "running_env": "testing",
            "odoo_test_option": "fake odoo config",
        },
    )
    def test_server_environment_disabled_overwrite_options_section_by_env(self):
        with self.set_config_dir("testfiles"):
            server_env._load_config()
            self.assertEqual(odoo_config["odoo_test_option"], "fake odoo config")
