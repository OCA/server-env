from odoo.tests import tagged

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase


@tagged("post_install", "-at_install")
class TestMailEnvironment(ServerEnvironmentCase):
    def test_outgoing_mail_server(self):
        mail_server = (
            self.env["ir.mail_server"]
            .with_context(active_test=False)
            .search([("name", "=", "Test Outgoing Mail Server")])
        )
        self.assertTrue(mail_server)
        self.assertEqual(mail_server.smtp_host, "localhost")
        self.assertEqual(mail_server.smtp_port, 25)
        self.assertEqual(mail_server.smtp_user, "test")
        self.assertEqual(mail_server.smtp_pass, "test123")

    def test_incoming_mail_server(self):
        mail_server = (
            self.env["fetchmail.server"]
            .with_context(active_test=False)
            .search([("name", "=", "Test Incoming Mail Server")])
        )
        self.assertTrue(mail_server)
        self.assertEqual(mail_server.server, "localhost")
        self.assertEqual(mail_server.port, 143)
        self.assertEqual(mail_server.user, "test")
        self.assertEqual(mail_server.password, "test123")
