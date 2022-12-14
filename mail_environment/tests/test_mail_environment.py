# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)


from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

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
