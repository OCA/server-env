# Copyright 2026 Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.server_environment.uninstall import restore_env_managed_columns

ENV_MANAGED_FIELDS = [
    "stripe_publishable_key",
    "stripe_secret_key",
    "stripe_webhook_secret",
]


def post_init_hook(env):
    # values are restored field by field (one write per field):
    # the required fields check would fail on active providers
    # as soon as the first field is written
    env["payment.provider"].with_context(
        strip_env_skip_check_required_if_provider=True
    )._preserve_not_env_managed_data(ENV_MANAGED_FIELDS)


def uninstall_hook(env):
    restore_env_managed_columns(env, "payment.provider", ENV_MANAGED_FIELDS)
