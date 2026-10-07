# Copyright 2026 Camptocamp (https://www.camptocamp.com)
from odoo.addons.server_environment.uninstall import restore_env_managed_columns


def uninstall_hook(env):
    """Restore database columns that server.env.mixin dropped for mail models.

    When mail_environment is uninstalled, ``ir.mail_server`` and
    ``fetchmail.server`` would be left without the columns that the ORM
    dropped when this addon was first installed. This hook recreates those
    columns and repopulates them with the current effective values so the
    database remains usable after removal.

    After uninstalling this module, an Odoo server restart is required.
    Field definitions referencing the compute methods of the mixin persist in memory
    until the Python process restarts.
    """
    restore_env_managed_columns(
        env,
        "ir.mail_server",
        [
            "smtp_host",
            "smtp_port",
            "smtp_user",
            "smtp_pass",
            "smtp_encryption",
            "smtp_authentication",
        ],
    )
    restore_env_managed_columns(
        env,
        "fetchmail.server",
        [
            "server",
            "port",
            "server_type",
            "user",
            "password",
            "is_ssl",
            "attach",
            "original",
        ],
    )
