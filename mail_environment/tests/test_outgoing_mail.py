from odoo.tools import sql

from odoo.addons.mail_environment.tests.common import MailEnvironmentCase
from odoo.addons.server_environment.tests.common import ServerEnvironmentCase
from odoo.addons.server_environment.uninstall import restore_env_managed_columns

mail_server_config = """
[outgoing_mail]
smtp_host = smtp.myserver.com
smtp_port = 587
smtp_user =
smtp_pass =
smtp_encryption = ssl

[outgoing_mail.mail_server1]
smtp_user = user1
smtp_pass = password1

[outgoing_mail.mail_server2]
smtp_user = user2
smtp_pass = password2
"""

_outgoing_config = """
[outgoing_mail.test_outgoing]
smtp_host = smtp.example.com
smtp_port = 587
smtp_encryption = starttls
smtp_authentication = login
smtp_user = testuser
smtp_pass = testpass
"""


class TestMailServerEnvironment(ServerEnvironmentCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mailServer = cls.env["ir.mail_server"]
        cls.mail_server1 = cls.mailServer.create({"name": "mail_server1"})
        cls.mail_server2 = cls.mailServer.create({"name": "mail_server2"})

    def test_mail_server_search_smtp_user(self):
        with self.load_config(public=mail_server_config):
            # Test basic properties
            self.assertEqual(self.mail_server1.smtp_user, "user1")
            self.assertEqual(self.mail_server2.smtp_user, "user2")

            # Test smtp_user search method
            self.assertIn(
                self.mail_server1,
                self.env["ir.mail_server"].search([("smtp_user", "=", "user1")]),
            )
            self.assertNotIn(
                self.mail_server1,
                self.env["ir.mail_server"].search([("smtp_user", "!=", "user1")]),
            )
            self.assertIn(
                self.mail_server2,
                self.env["ir.mail_server"].search([("smtp_user", "=", "user2")]),
            )
            self.assertNotIn(
                self.mail_server2,
                self.env["ir.mail_server"].search([("smtp_user", "!=", "user2")]),
            )
            self.assertIn(
                self.mail_server1,
                self.env["ir.mail_server"].search([("smtp_user", "ilike", "user")]),
            )
            self.assertIn(
                self.mail_server2,
                self.env["ir.mail_server"].search([("smtp_user", "ilike", "user")]),
            )

    def test_mail_server_search_smtp_host(self):
        with self.load_config(public=mail_server_config):
            # Test basic properties
            self.assertEqual(self.mail_server1.smtp_host, "smtp.myserver.com")
            self.assertEqual(self.mail_server2.smtp_host, "smtp.myserver.com")

            # Test smtp_user search method
            self.assertIn(
                self.mail_server1,
                self.env["ir.mail_server"].search(
                    [("smtp_host", "=", "smtp.myserver.com")]
                ),
            )
            self.assertNotIn(
                self.mail_server1,
                self.env["ir.mail_server"].search(
                    [("smtp_host", "!=", "smtp.myserver.com")]
                ),
            )
            self.assertIn(
                self.mail_server2,
                self.env["ir.mail_server"].search(
                    [("smtp_host", "=", "smtp.myserver.com")]
                ),
            )
            self.assertNotIn(
                self.mail_server2,
                self.env["ir.mail_server"].search(
                    [("smtp_host", "!=", "smtp.myserver.com")]
                ),
            )
            self.assertIn(
                self.mail_server1,
                self.env["ir.mail_server"].search([("smtp_host", "ilike", "myserver")]),
            )
            self.assertIn(
                self.mail_server2,
                self.env["ir.mail_server"].search([("smtp_host", "ilike", "myserver")]),
            )


class TestRestoreOutgoingMailColumns(MailEnvironmentCase):
    """Test restoration of outgoing mail columns during uninstall."""

    def test_restore_ir_mail_server_columns(self):
        """Outgoing mail columns are recreated and populated with config values."""
        field_names = [
            "smtp_host",
            "smtp_port",
            "smtp_encryption",
            "smtp_authentication",
            "smtp_user",
            "smtp_pass",
        ]
        server = self.env["ir.mail_server"].create({"name": "test_outgoing"})
        try:
            with self.load_config(public=_outgoing_config):
                restore_env_managed_columns(self.env, "ir.mail_server", field_names)
                table = self.env["ir.mail_server"]._table
                for field_name in field_names:
                    self.assertTrue(
                        sql.column_exists(self.env.cr, table, field_name),
                        f"Column {field_name} was not created",
                    )
                self.env.cr.execute(
                    "SELECT smtp_host, smtp_port, smtp_encryption,"
                    " smtp_authentication, smtp_user, smtp_pass"
                    " FROM ir_mail_server WHERE id = %s",
                    [server.id],
                )
                row = self.env.cr.dictfetchone()
                self.assertEqual(row["smtp_host"], "smtp.example.com")
                self.assertEqual(row["smtp_port"], 587)
                self.assertEqual(row["smtp_encryption"], "starttls")
                self.assertEqual(row["smtp_authentication"], "login")
                self.assertEqual(row["smtp_user"], "testuser")
                self.assertEqual(row["smtp_pass"], "testpass")
        finally:
            self._drop_columns("ir.mail_server", field_names)

    def test_restore_ir_mail_server_columns_with_default(self):
        """Columns are populated with default values when no config is loaded."""
        field_names = ["smtp_host", "smtp_port"]
        # Write via the inverse to set the x_smtp_host_env_default sparse field.
        server = self.env["ir.mail_server"].create(
            {"name": "test_default_outgoing", "smtp_host": "default.example.com"}
        )
        try:
            # No config loaded — values come from x_smtp_host_env_default.
            restore_env_managed_columns(self.env, "ir.mail_server", field_names)
            table = self.env["ir.mail_server"]._table
            self.assertTrue(sql.column_exists(self.env.cr, table, "smtp_host"))
            self.env.cr.execute(
                "SELECT smtp_host FROM ir_mail_server WHERE id = %s",
                [server.id],
            )
            self.assertEqual(self.env.cr.fetchone()[0], "default.example.com")
        finally:
            self._drop_columns("ir.mail_server", field_names)

    def test_restore_env_managed_columns_idempotent(self):
        """Calling restore_env_managed_columns twice is safe and idempotent."""
        field_names = ["smtp_host", "smtp_port"]
        self.env["ir.mail_server"].create({"name": "test_idempotent"})
        try:
            with self.load_config(public=_outgoing_config):
                restore_env_managed_columns(self.env, "ir.mail_server", field_names)
                # Second call must not raise or corrupt data.
                restore_env_managed_columns(self.env, "ir.mail_server", field_names)
            table = self.env["ir.mail_server"]._table
            for field_name in field_names:
                self.assertTrue(sql.column_exists(self.env.cr, table, field_name))
        finally:
            self._drop_columns("ir.mail_server", field_names)

    def test_restore_env_managed_columns_with_fallback_defaults(self):
        """Fields with no value can be restored with fallback values
        via field_defaults."""

        field_names = ["smtp_host"]
        server = self.env["ir.mail_server"].create({"name": "test_fallback"})
        try:
            # smtp_host has no config, no ORM default, and no env_default.
            # With field_defaults, it should be populated with the fallback value.
            restore_env_managed_columns(
                self.env,
                "ir.mail_server",
                field_names,
                field_defaults={"smtp_host": "fallback.example.com"},
            )
            table = self.env["ir.mail_server"]._table
            self.assertTrue(sql.column_exists(self.env.cr, table, "smtp_host"))
            self.env.cr.execute(
                "SELECT smtp_host FROM ir_mail_server WHERE id = %s",
                [server.id],
            )
            self.assertEqual(self.env.cr.fetchone()[0], "fallback.example.com")
        finally:
            self._drop_columns("ir.mail_server", field_names)

    def test_restore_env_managed_columns_no_fallback(self):
        """Fields with no value and no fallback are set to NULL."""

        field_names = ["smtp_host"]
        server = self.env["ir.mail_server"].create({"name": "test_no_value"})
        try:
            # smtp_host has no config, no default, and no field_defaults.
            # The column should be created and set to NULL.
            restore_env_managed_columns(self.env, "ir.mail_server", field_names)
            table = self.env["ir.mail_server"]._table
            self.assertTrue(sql.column_exists(self.env.cr, table, "smtp_host"))
            self.env.cr.execute(
                "SELECT smtp_host FROM ir_mail_server WHERE id = %s",
                [server.id],
            )
            self.assertIsNone(self.env.cr.fetchone()[0])
        finally:
            self._drop_columns("ir.mail_server", field_names)

    def test_restore_env_managed_columns_required_field_uses_model_default(self):
        """Fields with no value can be restored from the model default (if available)
        when no fallback is provided."""

        field_names = ["smtp_authentication"]
        server = self.env["ir.mail_server"].create({"name": "test_no_fallback"})
        try:
            # On supported Odoo versions smtp_authentication has a model default
            # ('login'). Restoring without field_defaults should therefore succeed by
            # using that effective value.
            restore_env_managed_columns(self.env, "ir.mail_server", field_names)
            self.env.cr.execute(
                "SELECT smtp_authentication FROM ir_mail_server WHERE id = %s",
                [server.id],
            )
            self.assertEqual(self.env.cr.fetchone()[0], "login")
        finally:
            # Manually drop in case the column was created.
            model = self.env["ir.mail_server"]
            if sql.column_exists(self.env.cr, model._table, "smtp_authentication"):
                self.env.cr.execute(
                    f'ALTER TABLE {model._table} DROP COLUMN "smtp_authentication"'
                )
