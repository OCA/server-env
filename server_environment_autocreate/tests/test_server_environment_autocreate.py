# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# Copyright 2024, 2025 XCG Consulting (https://xcg-consulting.fr).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
import os
from unittest.mock import patch

from odoo.orm.model_classes import add_to_registry
from odoo.tools.config import config  # type: ignore[import-untyped]

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

from ..models import server_env_mixin as server_env_mixin_2


class TestEnv(ServerEnvironmentCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load fake models ->/
        from .models import ExternalService, ExternalService2

        add_to_registry(cls.registry, ExternalService)
        add_to_registry(cls.registry, ExternalService2)
        cls.registry._setup_models__(
            cls.env.cr, ["external_service", "external_service_2"]
        )
        cls.registry.init_models(
            cls.env.cr,
            ["external_service", "external_service_2"],
            {"models_to_check": True},
        )
        cls.addClassCleanup(cls.registry.__delitem__, "external_service")
        cls.addClassCleanup(cls.registry.__delitem__, "external_service_2")

        cls.env["external_service"].create([{"name": "ftp2", "description": "another"}])

    @patch.dict(config.options, {"running_env": "autocreate"})
    def test_autocreate(self):
        config_dir = os.path.join(os.path.dirname(__file__), "files")
        with (
            self.load_config(config_dir=config_dir),
            self.load_config(
                config_dir=config_dir, serv_config_class=server_env_mixin_2
            ),
        ):
            # Explicit call to _register_hook needed for the tests only.
            self.env["external_service"]._register_hook()
            self.env["external_service_2"]._register_hook()

            # auto created record
            record = self.env.ref(
                "__server_environment_autocreate__.external_service.ftp_1"
            )
            self.assertEqual(record.name, "ftp 1")
            self.assertEqual(record.description, "ftp server")
            self.assertEqual(record.host, "sftp.example.com")
            self.assertEqual(record.user, "foo")
            self.assertEqual(record.password, "bar")

            # created record
            # Test it has no xmlid
            record = self.env.ref(
                "__server_environment_autocreate__.external_service.ftp2", False
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

            # assert no creation if autocreate to false on model
            self.assertFalse(
                self.env.ref(
                    "__server_environment_autocreate__.external_service_2.ftp",
                    False,
                )
            )
            self.assertFalse(
                self.env["external_service_2"].search([("name", "=", "ftp")])
            )
