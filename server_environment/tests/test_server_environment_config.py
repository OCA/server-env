from odoo.orm.model_classes import add_to_registry
from odoo.tests import Form, tagged

from . import common

CONFIG = """
[external_service.ftp1]
host=sftp.example.com
user=foo
password=bar

[external_service.ftp2]
host=sftp2.example.com
user=monty
password=python

[external_service.ftp3]
host=sftp3.example.com
user=monty
"""


# Test need to be run post install otherwise the _register_hook is not called yet
@tagged("post_install", "-at_install")
class TestEnv(common.ServerEnvironmentCase):
    def test_load_config(self):
        from .models import ExternalService

        add_to_registry(self.registry, ExternalService)
        self.registry._setup_models__(self.env.cr, ["external.service"])
        self.registry.init_models(
            self.env.cr, ["external.service"], {"models_to_check": True}
        )
        ftp1 = self.env["external.service"].create(
            {
                "name": "ftp1",
                "description": "Description ftp1",
                "host": "localhost1",
                "user": "user1",
                "password": "pass1",
            }
        )
        ftp2 = self.env["external.service"].create(
            {
                "name": "ftp2",
                "description": "Description ftp2",
                "host": "localhost2",
                "user": "user2",
                "password": "pass2",
            }
        )
        ftp3 = self.env["external.service"].create(
            {
                "name": "ftp3",
                "description": "Description ftp3",
                "host": "localhost3",
                "user": "user3",
            }
        )
        ftp1.invalidate_recordset()
        ftp2.invalidate_recordset()
        ftp3.invalidate_recordset()
        with self.load_config(public=CONFIG):
            self.assertEqual(ftp1.name, "ftp1")
            self.assertEqual(ftp1.description, "Description ftp1")
            self.assertEqual(ftp1.host, "sftp.example.com")
            self.assertEqual(ftp1.user, "foo")
            self.assertEqual(ftp1.password, "bar")

            self.assertEqual(ftp2.name, "ftp2")
            self.assertEqual(ftp2.description, "Description ftp2")
            self.assertEqual(ftp2.host, "sftp2.example.com")
            self.assertEqual(ftp2.user, "monty")
            self.assertEqual(ftp2.password, "python")

            self.assertEqual(ftp3.name, "ftp3")
            self.assertEqual(ftp3.description, "Description ftp3")
            self.assertEqual(ftp3.host, "sftp3.example.com")
            self.assertEqual(ftp3.user, "monty")
            self.assertEqual(ftp3.password, "computed_password")

            with Form(ftp1) as f:
                f.description = "New description"
                with self.assertRaisesRegex(
                    AssertionError, "can't write on readonly field 'host'"
                ):
                    f.host = "newhost"
                with self.assertRaisesRegex(
                    AssertionError, "can't write on readonly field 'user'"
                ):
                    f.user = "newuser"
                with self.assertRaisesRegex(
                    AssertionError, "can't write on readonly field 'password'"
                ):
                    f.password = "newpass"
