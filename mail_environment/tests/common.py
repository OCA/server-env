from psycopg2 import sql as pg_sql

from odoo.tools import sql

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase


class MailEnvironmentCase(ServerEnvironmentCase):
    def _drop_columns(self, model_name, field_names):
        """Drop columns created by restore_env_managed_columns (test cleanup)."""
        model = self.env[model_name]
        cr = self.env.cr
        for field_name in field_names:
            if sql.column_exists(cr, model._table, field_name):
                cr.execute(
                    pg_sql.SQL("ALTER TABLE {} DROP COLUMN {}").format(
                        pg_sql.Identifier(model._table),
                        pg_sql.Identifier(field_name),
                    )
                )
