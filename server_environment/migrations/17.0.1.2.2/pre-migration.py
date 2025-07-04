# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import json
import logging

from psycopg2 import sql
from psycopg2.extras import execute_values

_logger = logging.getLogger(__name__)


def _get_impacted_table_names(cr):
    query = """
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE COLUMN_NAME = 'server_env_defaults';
    """
    cr.execute(query)
    return [row[0] for row in cr.fetchall()]


def _get_values_to_fix(cr, table):
    query = sql.SQL(
        """
            SELECT id, server_env_defaults
            FROM {table}
            WHERE server_env_defaults
            IS NOT NULL;
        """
    )
    formatted_query = query.format(table=sql.Identifier(table))
    cr.execute(formatted_query)
    return cr.fetchall()


def _get_fixed_values(cr, values):
    new_values = []
    for _id, defaults in values:
        # defaults are string dicts
        defaults = json.loads(defaults)
        new_defaults = {}
        for key, value in defaults.items():
            # Only fix keys that weren't already fixed
            # Makes this idempotent.
            if key.endswith("_env_default") and not key.startswith("x_"):
                new_defaults[f"x_{key}"] = value
            else:
                new_defaults[key] = value
        # dump dict in a string
        new_values.append((_id, json.dumps(new_defaults)))
    return new_values


def _apply_new_values(cr, table, values):
    # Doing the formatting in 2 steps, this is on purpose.
    query = f"""
        UPDATE {table}
        SET server_env_defaults = c.server_env_defaults
        FROM (VALUES %s)
        AS c(id, server_env_defaults)
        WHERE {table}.id = c.id
    """
    execute_values(cr, query, values)


def fix_server_env_defaults(cr):
    for table_name in _get_impacted_table_names(cr):
        _logger.info(f"Fixing server_env_defaults on '{table_name}'")
        old_values = _get_values_to_fix(cr, table_name)
        new_values = _get_fixed_values(cr, old_values)
        _apply_new_values(cr, table_name, new_values)


def migrate(cr, version):
    fix_server_env_defaults(cr)
