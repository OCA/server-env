# Copyright 2016-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import psycopg2

from odoo.modules.module import get_resource_path
from odoo.tests.common import Form
from odoo.tools import convert_file
from odoo.tools.misc import mute_logger

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase


class TestEnv(ServerEnvironmentCase):
    def setUp(self):
        super().setUp()
        self.IAP = self.env["iap.account"]
        self.env_config = (
            "[iap_account.account_1]\n"
            "service_name=partner_autocomplete_1\n"
            "account_token=my_secret_token_1\n"
            "[iap_account.account_2]\n"
            "service_name=partner_autocomplete_2\n"
            "account_token=my_secret_token_2\n"
            "[iap_account.account_xml]\n"
            "service_name=partner_autocomplete_xml\n"
            "account_token=my_secret_token_xml\n"
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

    def test_create_account_from_config(self):
        """Get account data from config"""
        with self.load_config(public=self.env_config):
            account = self.IAP.create({"tech_name": "account_1"})
            self.assertEqual(account.service_name, "partner_autocomplete_1")
            self.assertEqual(account.account_token, "my_secret_token_1")
            # `tech_name` must be unique
            with self.assertRaises(psycopg2.IntegrityError):
                with mute_logger("odoo.sql_db"), self.cr.savepoint():
                    self.IAP.create({"tech_name": "account_1"})

    def test_create_account_not_in_config(self):
        """We can set account data that is not in config file"""
        with self.load_config(public=self.env_config):
            account = self.IAP.create(
                {
                    "tech_name": "account_4",
                    "service_name": "new_partner_autocomplete",
                    "account_token": "my_new_secret_token",
                }
            )
            self.assertEqual(account.service_name, "new_partner_autocomplete")
            self.assertEqual(account.account_token, "my_new_secret_token")

    # TODO: should it be overriden on xml import?
    # def test_override_xmldata(self):
    #     with self.load_config(public=self.env_config):
    #         self._load_xml("server_environment_iap", "tests/config_iap_test.xml")
    #         account = self.IAP.search([("tech_name", "=", "account_xml")])
    #         self.assertEqual(account.service_name, "partner_autocomplete_xml")
    #         self.assertEqual(account.account_token, "my_secret_token_xml")

    def test_update_account_data(self):
        """We can't set account data that is in config file"""
        with self.load_config(public=self.env_config):
            # when creating, the value is overridden by config file
            account = self.IAP.create(
                {
                    "tech_name": "account_2",
                }
            )
            account_form = Form(account)
            self.assertEqual(account.service_name, "partner_autocomplete_2")
            self.assertEqual(account.account_token, "my_secret_token_2")
            with self.assertRaises(AssertionError):
                account_form.service_name = "new_partner_autocomplete"
            with self.assertRaises(AssertionError):
                account_form.account_token = "my_new_secret_token"
