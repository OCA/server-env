# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from configparser import ConfigParser
from unittest.mock import patch

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.server_environment.models import server_env_mixin


class TestGmailEnvironment(BaseCommon):
    def test_refresh_token_from_environment(self):
        config = ConfigParser()
        config.read_string(
            """
[outgoing_mail.gmail_smtp_server]
smtp_host = smtp.gmail.com
smtp_port = 587
smtp_user = example@gmail.com
smtp_encryption = starttls
smtp_authentication = gmail
google_gmail_refresh_token = environment-refresh-token
"""
        )
        server = self.env["ir.mail_server"].create({"name": "gmail_smtp_server"})
        with patch.object(server_env_mixin, "serv_config", config):
            server.invalidate_recordset(list(server._server_env_fields))
            self.assertEqual(server.smtp_authentication, "gmail")
            self.assertEqual(server.smtp_host, "smtp.gmail.com")
            self.assertEqual(server.smtp_user, "example@gmail.com")
            self.assertEqual(server.smtp_port, 587)
            self.assertEqual(
                server.google_gmail_refresh_token, "environment-refresh-token"
            )
            server.google_gmail_refresh_token = "database-refresh-token"
            server.invalidate_recordset(["google_gmail_refresh_token"])
            self.assertEqual(
                server.google_gmail_refresh_token, "environment-refresh-token"
            )

    def test_refresh_token_without_environment(self):
        with patch.object(server_env_mixin, "serv_config", ConfigParser()):
            server = self.env["ir.mail_server"].create(
                {
                    "name": "database_gmail_server",
                    "google_gmail_refresh_token": "database-refresh-token",
                }
            )
            server.invalidate_recordset(["google_gmail_refresh_token"])
            self.assertEqual(
                server.google_gmail_refresh_token, "database-refresh-token"
            )
