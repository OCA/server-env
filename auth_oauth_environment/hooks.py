# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    Provider = env["auth.oauth.provider"]
    for provider in Provider.search([("tech_name", "=", False)]):
        provider.tech_name = Provider._normalize_tech_name(provider.name)
    # keep what was set before install for providers missing from the config
    Provider._preserve_not_env_managed_data(["client_id", "enabled"])
