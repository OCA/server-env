# Copyright 2024 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)


from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

custom_config = """
[ir.config_parameter]
microsoft_outlook_client_id = YOUR_OFFICE365_CLIENT_ID
microsoft_outlook_client_secret = YOUR_OFFICE365_CLIENT_SECRET

[outgoing_mail.office365_smtp_server]
smtp_host = smtp.office365.com
smtp_port = 587
smtp_user = example@yourdomain.com
smtp_encryption = starttls
smtp_authentication = outlook
"""


class TestMailEnvironment(ServerEnvironmentCase):
    def test_mailserver(self):
        mailserver = self.env["ir.mail_server"].create(
            {"name": "office365_smtp_server"}
        )
        with self.load_config(public=custom_config):
            # Test basic properties
            self.assertEqual(mailserver.smtp_host, "smtp.office365.com")
            self.assertEqual(mailserver.smtp_port, 587)
            self.assertEqual(mailserver.smtp_user, "example@yourdomain.com")
            self.assertEqual(mailserver.smtp_encryption, "starttls")
            self.assertEqual(mailserver.smtp_authentication, "outlook")
