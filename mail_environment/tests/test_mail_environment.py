# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)


from odoo.tools import sql

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase
from odoo.addons.server_environment.uninstall import restore_env_managed_columns

fetchmail_config = """
[incoming_mail.fetchmail1]
server = safe_server
port = 993
server_type = imap
is_ssl = 1
attach = 1
original = 1
user = admin
password = admin
state = done
priority = 1
active = 1

[incoming_mail.fetchmail2]
server = unsafe_server
port = 143
server_type = imap
is_ssl = 0
attach = 1
original = 1
user = admin
password = admin
state = done
priority = 1
active = 1
"""


class TestMailEnvironment(ServerEnvironmentCase):
    def test_fetchmail_search_is_ssl(self):
        fetchmail1 = self.env["fetchmail.server"].create({"name": "fetchmail1"})
        fetchmail2 = self.env["fetchmail.server"].create({"name": "fetchmail2"})
        with self.load_config(public=fetchmail_config):
            # Test basic properties
            self.assertTrue(fetchmail1.is_ssl)
            self.assertEqual(fetchmail1.port, 993)
            self.assertFalse(fetchmail2.is_ssl)
            self.assertEqual(fetchmail2.port, 143)

            # Test is_ssl search method
            self.assertIn(
                fetchmail1, self.env["fetchmail.server"].search([("is_ssl", "=", True)])
            )
            self.assertIn(
                fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "!=", False)]),
            )
            self.assertNotIn(
                fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "=", False)]),
            )
            self.assertNotIn(
                fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "!=", True)]),
            )
            self.assertNotIn(
                fetchmail2, self.env["fetchmail.server"].search([("is_ssl", "=", True)])
            )
            self.assertNotIn(
                fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "!=", False)]),
            )
            self.assertIn(
                fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "=", False)]),
            )
            self.assertIn(
                fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "!=", True)]),
            )


_outgoing_config = """
[outgoing_mail.test_outgoing]
smtp_host = smtp.example.com
smtp_port = 587
smtp_encryption = starttls
smtp_authentication = login
smtp_user = testuser
smtp_pass = testpass
"""

_incoming_config = """
[incoming_mail.test_incoming]
server = imap.example.com
port = 993
server_type = imap
is_ssl = 1
user = imap_user
password = imap_pass
attach = 1
original = 0
"""


class TestRestoreEnvManagedColumns(ServerEnvironmentCase):
    """Test column restoration performed by the uninstall hook."""

    def _drop_columns(self, model_name, field_names):
        """Drop columns created by restore_env_managed_columns (test cleanup)."""
        model = self.env[model_name]
        cr = self.env.cr
        for field_name in field_names:
            if sql.column_exists(cr, model._table, field_name):
                cr.execute(  # noqa: S608
                    f'ALTER TABLE {model._table} DROP COLUMN "{field_name}"'
                )

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

    def test_restore_fetchmail_server_columns(self):
        """Incoming mail columns are recreated and populated with config values."""
        field_names = [
            "server",
            "port",
            "server_type",
            "is_ssl",
            "user",
            "password",
            "attach",
            "original",
        ]
        fetchmail = self.env["fetchmail.server"].create({"name": "test_incoming"})
        try:
            with self.load_config(public=_incoming_config):
                restore_env_managed_columns(self.env, "fetchmail.server", field_names)
                table = self.env["fetchmail.server"]._table
                for field_name in field_names:
                    self.assertTrue(
                        sql.column_exists(self.env.cr, table, field_name),
                        f"Column {field_name} was not created",
                    )
                self.env.cr.execute(
                    'SELECT server, port, server_type, is_ssl, "user",'
                    " password, attach, original"
                    " FROM fetchmail_server WHERE id = %s",
                    [fetchmail.id],
                )
                row = self.env.cr.dictfetchone()
                self.assertEqual(row["server"], "imap.example.com")
                self.assertEqual(row["port"], 993)
                self.assertEqual(row["server_type"], "imap")
                self.assertTrue(row["is_ssl"])
                self.assertEqual(row["user"], "imap_user")
                self.assertEqual(row["password"], "imap_pass")
                self.assertTrue(row["attach"])
                self.assertFalse(row["original"])
        finally:
            self._drop_columns("fetchmail.server", field_names)

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
            column_exists = sql.column_exists(self.env.cr, table, "smtp_host")
            self.assertTrue(column_exists)
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
            column_exists = sql.column_exists(self.env.cr, table, "smtp_host")
            self.assertTrue(column_exists)
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
                self.env.cr.execute(  # noqa: S608
                    f'ALTER TABLE {model._table} DROP COLUMN "smtp_authentication"'
                )
