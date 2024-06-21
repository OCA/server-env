# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# Copyright 2024 XCG Consulting (https://xcg-consulting.fr).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from unittest.mock import patch

from odoo_test_helper import FakeModelLoader

from odoo.tests import tagged
from odoo.tools.config import config as odoo_config

from .. import server_env
from ..models import server_env_mixin
from . import common


# Test need to be run post install otherwise the _register_hook is not called yet
@tagged("post_install", "-at_install")
class TestEnv(common.ServerEnvironmentCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load fake models ->/
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ExternalService

        cls.loader.update_registry((ExternalService,))
        cls.env["external_service"].create([{"name": "ftp2", "description": "another"}])

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    @patch.dict(odoo_config.options, {"running_env": "autocreate"})
    def test_autocreate(self):
        original_serv_config = server_env_mixin.serv_config
        try:
            with self.set_config_dir("testfiles"):
                parser = server_env._load_config()
                server_env_mixin.serv_config = parser
                # Needed to force _register_hook with auto creation
                self.loader.update_registry(tuple())

                # auto created record
                record = self.env.ref("__server_environment__.external_service.ftp")
                self.assertEqual(record.name, "ftp")
                self.assertEqual(record.description, "ftp server")
                self.assertEqual(record.host, "sftp.example.com")
                self.assertEqual(record.user, "foo")
                self.assertEqual(record.password, "bar")

                # create record in setupClass
                # Test it has no xmlid
                record = self.env.ref(
                    "__server_environment__.external_service.ftp2", False
                )
                self.assertFalse(record)
                # look for it
                record = self.env["external_service"].search([("name", "=", "ftp2")])
                self.assertEqual(len(record), 1)
                self.assertEqual(record.name, "ftp2")
                # different from __autocreate dict as it is created in setUpClass
                self.assertEqual(record.description, "another")
                self.assertEqual(record.host, "sftp2.example.com")
                self.assertEqual(record.user, "monty")
                self.assertEqual(record.password, "python")
        finally:
            server_env_mixin.serv_config = original_serv_config
