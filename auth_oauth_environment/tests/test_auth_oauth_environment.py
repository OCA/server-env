# Copyright 2024 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

from ..hooks import post_init_hook

custom_config = """
[auth_oauth.provider_google]
client_id = YOUR_OAUTH_GOOGLE_CLIENT_ID
enabled = True
"""


class TestAuthOAuthEnvironment(ServerEnvironmentCase):
    def setUp(self):
        super().setUp()
        self.provider_google = self.env.ref("auth_oauth.provider_google")

    def test_auth_oauth_provider(self):
        with self.load_config(public=custom_config):
            self.assertEqual(
                self.provider_google.client_id, "YOUR_OAUTH_GOOGLE_CLIENT_ID"
            )
            self.assertTrue(self.provider_google.enabled)

    def test_search_enabled(self):
        Provider = self.env["auth.oauth.provider"]
        with self.load_config(public=custom_config):
            self.assertEqual(
                Provider.search([("enabled", "=", True)]), self.provider_google
            )
            self.assertNotIn(
                self.provider_google, Provider.search([("enabled", "!=", True)])
            )

    def test_rename_keeps_tech_name(self):
        self.provider_google.name = "Google"
        self.assertEqual(self.provider_google.tech_name, "provider_google")

    def test_post_init_hook_keeps_db_values(self):
        corp = self.env["auth.oauth.provider"].create(
            {
                "name": "Corp SSO",
                "auth_endpoint": "https://sso.example.com/auth",
                "validation_endpoint": "https://sso.example.com/validate",
                "body": "Log in with Corp",
            }
        )
        # state of the table before install: values in the columns only
        self.env.cr.execute(
            """
            UPDATE auth_oauth_provider
            SET enabled = true, client_id = 'DB-ID', server_env_defaults = NULL,
                tech_name = CASE WHEN id = %s THEN NULL ELSE tech_name END
            WHERE id IN %s
            """,
            (corp.id, (corp.id, self.provider_google.id)),
        )
        self.env.invalidate_all()
        with self.load_config(public=custom_config):
            post_init_hook(self.env)
            self.env.invalidate_all()
            self.assertEqual(corp.tech_name, "corp_sso")
            self.assertTrue(corp.enabled)
            self.assertEqual(corp.client_id, "DB-ID")
            self.assertEqual(
                self.provider_google.client_id, "YOUR_OAUTH_GOOGLE_CLIENT_ID"
            )
