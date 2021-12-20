# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.modules.module import get_resource_path
from odoo.tests import tagged
from odoo.tools import convert_file

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

from ..models import iap_account


@tagged("post_install", "-at_install")
class TestEnv(ServerEnvironmentCase):
    def setUp(self):
        super().setUp()
        self.IAP = self.env["iap.account"]
        self.env_config = (
            "[iap.account]\n" "iap_from_config=config_value\n" "iap_empty=\n"
        )
        self.service_name = "iap_from_config"
        self.account_token = "config_value"
        self.some_service = "some.service"
        self.some_token = "some.token"

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

    def _search_account(self, service, token):
        return self.IAP.search(
            [("service_name", "=", service), ("account_token", "=", token)]
        )

    def test_empty(self):
        """Empty config values cause error"""
        with self.load_config(public=self.env_config, serv_config_class=iap_account):
            with self.assertRaises(UserError):
                self.IAP.get("iap_empty")
            iap_nonexistant = self.IAP.get("iap_nonexistant")
            self.assertTrue(iap_nonexistant.account_token)

    def test_get_account(self):
        """Get account data from config"""
        with self.load_config(public=self.env_config, serv_config_class=iap_account):
            # it's not in db
            res = self._search_account(self.service_name, self.account_token)
            self.assertFalse(res)
            # read so it's created in db
            account = self.IAP.get("iap_from_config")
            self.assertEqual(account.account_token, "config_value")
            self.assertEqual(len(account), 1)

    def test_override_xmldata(self):
        with self.load_config(public=self.env_config, serv_config_class=iap_account):
            self._load_xml("server_environment_iap", "tests/config_iap_test.xml")
            self.assertEqual(
                self.IAP.get("iap_from_config").account_token, "config_value"
            )

    def test_set_param_1(self):
        """We can't set account data that is in config file"""
        with self.load_config(public=self.env_config, serv_config_class=iap_account):
            # when creating, the value is overridden by config file
            self.IAP.create(
                {"service_name": "iap_from_config", "account_token": "new_value"}
            )
            acc = self.IAP.get("iap_from_config")
            self.assertEqual(acc.account_token, "config_value")
            # when writing, the value is overridden by config file
            res = self._search_account(self.service_name, self.account_token)
            self.assertEqual(len(res), 1)
            res.write({"account_token": "new_value"})
            acc = self.IAP.get("iap_from_config")
            self.assertEqual(acc.account_token, "config_value")
            # unlink works normally...
            res = self._search_account(self.service_name, self.account_token)
            self.assertEqual(len(res), 1)
            res.unlink()
            res = self._search_account(self.service_name, self.account_token)
            self.assertEqual(len(res), 0)
            # but the value is recreated when getting param again
            acc = self.IAP.get("iap_from_config")
            self.assertEqual(acc.account_token, "config_value")
            self.assertEqual(len(acc), 1)

    def test_set_param_2(self):
        """We can set parameters that are not in config file"""
        with self.load_config(public=self.env_config, serv_config_class=iap_account):
            self.IAP.create(
                {"service_name": "some.service", "account_token": "some.token"}
            )
            self.assertEqual(self.IAP.get("some.service").account_token, "some.token")
