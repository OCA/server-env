# Copyright 2024 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)


from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

custom_config = """
[auth_oauth.provider_google]
client_id = YOUR_OAUTH_GOOGLE_CLIENT_ID
enabled = True
"""


class TestAuthOAuthEnvironment(ServerEnvironmentCase):
    def test_auth_oauth_provider(self):
        provider_google = self.env.ref("auth_oauth.provider_google", False)
        with self.load_config(public=custom_config):
            self.assertEqual(provider_google.client_id, "YOUR_OAUTH_GOOGLE_CLIENT_ID")
            self.assertTrue(provider_google.enabled)
