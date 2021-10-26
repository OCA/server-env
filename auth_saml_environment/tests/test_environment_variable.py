# Copyright 2021 Camptocamp (https://www.camptocamp.com).
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.tools.config import config as odoo_config

from odoo.addons.server_environment import server_env
from odoo.addons.server_environment.tests.common import ServerEnvironmentCase


@patch.dict(odoo_config.options, {"running_env": "testing"})
class TestEnvironmentVariables(ServerEnvironmentCase):
    def test_env_variables(self):
        env_var = (
            "[auth_saml_provider.sample]\n"
            "idp_metadata=foo\n"
            "sp_baseurl=bar\n"
            "sp_pem_public_path=file1.txt\n"
            "sp_pem_private_path=file2.txt"
        )
        with self.set_config_dir(None), self.set_env_variables(env_var):
            parser = server_env._load_config()
            self.assertEqual(
                list(parser.keys()), ["DEFAULT", "auth_saml_provider.sample"]
            )
            self.assertDictEqual(
                dict(parser["auth_saml_provider.sample"].items()),
                {
                    "idp_metadata": "foo",
                    "sp_baseurl": "bar",
                    "sp_pem_public_path": "file1.txt",
                    "sp_pem_private_path": "file2.txt",
                },
            )
