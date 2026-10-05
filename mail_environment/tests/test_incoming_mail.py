# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo.tools import sql

from odoo.addons.mail_environment.tests.common import MailEnvironmentCase
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


class TestFetchMailEnvironment(ServerEnvironmentCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.FetchmailServer = cls.env["fetchmail.server"]
        cls.fetchmail1 = cls.FetchmailServer.create({"name": "fetchmail1"})
        cls.fetchmail2 = cls.FetchmailServer.create({"name": "fetchmail2"})

    def test_fetchmail_search_is_ssl(self):
        with self.load_config(public=fetchmail_config):
            # Test basic properties
            self.assertTrue(self.fetchmail1.is_ssl)
            self.assertEqual(self.fetchmail1.port, 993)
            self.assertFalse(self.fetchmail2.is_ssl)
            self.assertEqual(self.fetchmail2.port, 143)

            # Test is_ssl search method
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "=", True)]),
            )
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "!=", False)]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "=", False)]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "!=", True)]),
            )
            self.assertNotIn(
                self.fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "=", True)]),
            )
            self.assertNotIn(
                self.fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "!=", False)]),
            )
            self.assertIn(
                self.fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "=", False)]),
            )
            self.assertIn(
                self.fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "!=", True)]),
            )

    def test_fetchmail_search_server_type(self):
        with self.load_config(public=fetchmail_config):
            # Test server_type search method
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "=", "imap")]),
            )
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "!=", "pop3")]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "=", "pop3")]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "!=", "imap")]),
            )
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search(
                    [("server_type", "=ilike", "IMAP")]
                ),
            )
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "ilike", "IM")]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "ilike", "POP")]),
            )


class TestRestoreIncomingMailColumns(MailEnvironmentCase):
    """Test restoration of incoming mail columns during uninstall."""

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
