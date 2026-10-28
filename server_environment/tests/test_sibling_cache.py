# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo.exceptions import ValidationError
from odoo.orm.model_classes import add_to_registry
from odoo.tests import tagged

from . import common


# The test model's table is rolled back but the model stays in the
# registry: at install, the next module loading would find it tableless
@tagged("post_install", "-at_install")
class TestSiblingCache(common.ServerEnvironmentCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from .models import ExternalService

        add_to_registry(cls.registry, ExternalService)
        cls.registry._setup_models__(cls.env.cr, ["external.service"])
        cls.registry.init_models(
            cls.env.cr, ["external.service"], {"models_to_check": True}
        )

    def setUp(self):
        super().setUp()
        self.service = self.env["external.service"].create(
            {
                "name": "my_service",
                "description": "Description my_service",
                "host": "localhost",
                "user": "foo",
            }
        )
        # Start from an empty cache, as a web client save or an RPC call does
        self.service.invalidate_recordset()

    def test_constraint_reads_sibling_env_field_from_config(self):
        """A sibling defined in the configuration is not read as empty."""
        config = "[external_service.my_service]\nuser=from_config\n"
        with self.load_config(public=config):
            self.service.write({"host": "other.example.com"})

    def test_constraint_reads_sibling_env_field_from_default(self):
        """Siblings with a stored default (``user``) or a ``compute_default``
        (``password``) are not read as empty."""
        self.service.write({"host": "other.example.com"})

    def test_constraint_still_raises(self):
        """The constraint is still enforced with the sibling's actual value."""
        self.service.write({"user": False})
        self.service.invalidate_recordset()
        with self.assertRaises(ValidationError):
            self.service.write({"host": "other.example.com"})
