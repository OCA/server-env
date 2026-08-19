# Copyright 2026 Camptocamp (https://www.camptocamp.com)
import logging

from odoo.tools import SQL, sql

_logger = logging.getLogger(__name__)


def restore_env_managed_columns(env, model_name, field_names, field_defaults=None):
    """Restore database columns for fields formerly managed via server.env.mixin.

    When an addon binds ``server.env.mixin`` to an existing model, the ORM
    drops the original stored columns.  Call this helper from an
    ``uninstall_hook`` so those columns are recreated and repopulated
    with their current effective values before the addon is removed.

    The hook must run *while* the module's ORM extensions are still active
    (guaranteed by Odoo's uninstall sequence: hooks execute before
    ``Module.module_uninstall()``), so the env-computed fields are still
    readable and their values can be written back to freshly created columns.

    The operation is idempotent: calling it multiple times will not fail.

    **Defaults:** If a restored field value is NULL/empty, the helper will
    use the fallback from ``field_defaults`` (if provided) or the field's
    ORM-level default (if defined).

    Note: ``field.required`` is set to False by the mixin, so we cannot detect
    which fields are required. Provide explicit ``field_defaults`` for fields
    that must have values.

    :param str model_name: dotted model name, e.g. ``"ir.mail_server"``
    :param field_names: iterable of field names whose columns to restore
    :param dict field_defaults: optional mapping of field name to fallback
        value used when restoring a column that has no effective env-computed
        value, e.g. ``{"smtp_authentication": "<login>"}``
    """
    model = env[model_name]
    cr = env.cr
    field_defaults = field_defaults or {}

    for field_name in field_names:
        field = model._fields.get(field_name)
        if field is None:
            _logger.warning(
                "restore_env_managed_columns: field %r not found on %s, skipping",
                field_name,
                model_name,
            )
            continue
        column_type = field.column_type
        if column_type is None:
            _logger.warning(
                "restore_env_managed_columns: "
                "field %r on %s has no SQL column type, skipping",
                field_name,
                model_name,
            )
            continue
        table = model._table
        if not sql.column_exists(cr, table, field_name):
            sql.create_column(cr, table, field_name, column_type[1], field.string)
            _logger.info(
                "restore_env_managed_columns: created column %s.%s (%s)",
                table,
                field_name,
                column_type[1],
            )
        # Repopulate every existing record with the current computed value.
        # The hook runs while the ORM extensions are still active, so the
        # env-computed field is still readable via the normal accessor.
        for record in model.search([]):
            value = record[field_name]
            # The ORM returns False for NULL on non-boolean fields; map
            # that back to None so psycopg2 writes a proper SQL NULL.
            if value is False and field.type != "boolean":
                value = None
            elif value == "":
                value = None

            # Try to get a default value if we have None.
            # Note: field.required is False after mixin transformation,
            # so we apply defaults for all None values when available.
            if value is None:
                if field_name in field_defaults:
                    value = field_defaults[field_name]
                elif field_name in model.default_get([field_name]):
                    value = model.default_get([field_name])[field_name]

            cr.execute(
                SQL(
                    "UPDATE %s SET %s = %s WHERE id = %s",
                    SQL.identifier(table),
                    SQL.identifier(field_name),
                    value,
                    record.id,
                )
            )
