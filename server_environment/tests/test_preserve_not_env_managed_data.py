# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from . import common


class TestPreserveNotEnvManagedData(common.ServerEnvironmentCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Avoid import errors by other repos depending on server env test classes
        from odoo_test_helper import FakeModelLoader

        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        cls._origin_fields = {}
        for model in ("res.partner", "res.users"):
            cls._origin_fields[model] = set(dir(cls.env[model].__class__))

    def remove_mixin_fields(self):
        """Clean up what FakeModelLoader.restore_registry() leaves behind.

        It skips "x_"-prefixed fields (e.g. x_city_env_default) and never
        touches non-field attributes (e.g. _inverse_server_env_city).
        """
        for model in ("res.partner", "res.users"):
            extra = set(self.env[model].__class__.__dict__) - self._origin_fields[model]
            for attr in extra:
                delattr(self.env[model].__class__, attr)

    def setUp(self):
        super().setUp()
        from .fake_models import FakePartner

        self.loader.update_registry((FakePartner,))
        self.addCleanup(self.loader.restore_registry)
        self.addCleanup(self.remove_mixin_fields)
        # Deliberately not setting "city" here: writing it would already
        # populate x_city_env_default through the mixin's inverse method,
        # which would defeat the "no default yet" scenario below.
        self.partner = self.env["res.partner"].create({"name": "Test partner"})

    def _set_raw_city_column(self, value):
        """Bypass the ORM to simulate a stale/orphaned raw column value.

        Once a field is taken over by the mixin it becomes non-stored, so
        the ORM never reads or writes its physical column again. The column
        itself is never dropped though, so it can keep holding old data from
        before the field became server-env managed.
        """
        self.env.cr.execute(
            "UPDATE res_partner SET city = %s WHERE id = %s",
            (value, self.partner.id),
        )
        self.partner.invalidate_recordset(["city"])

    def test_preserve_rescues_value_when_no_default_yet(self):
        """Rescue the raw column value when there is no default yet.

        First-time adoption: no default stored yet, so the raw column
        value must be rescued into the new default field.
        """
        self._set_raw_city_column("Legacy Raw City")
        self.env["res.partner"]._preserve_not_env_managed_data(["city"])
        self.partner.invalidate_recordset()
        self.assertEqual(self.partner.x_city_env_default, "Legacy Raw City")
        self.assertEqual(self.partner.city, "Legacy Raw City")

    def test_preserve_does_not_overwrite_existing_default(self):
        """Do not overwrite a default value that is already set.

        A default already set (e.g. because the field was already
        server-env managed by another module before) must not be clobbered
        by a stale raw column value.
        """
        # Simulate the field having already been server-env managed: a
        # legitimate, up to date default is already stored.
        self.partner.write({"city": "Current Default City"})
        self.assertEqual(self.partner.x_city_env_default, "Current Default City")
        # The underlying (now unused) raw column still holds ancient data
        # from before the field became non-stored.
        self._set_raw_city_column("Ancient Stale City")
        self.env["res.partner"]._preserve_not_env_managed_data(["city"])
        self.partner.invalidate_recordset()
        self.assertEqual(self.partner.x_city_env_default, "Current Default City")
        self.assertEqual(self.partner.city, "Current Default City")

    def test_preserve_ignores_unknown_column(self):
        """Fields without a matching raw column are silently skipped."""
        # Must not raise even though the field name doesn't exist as a
        # column on the table.
        self.env["res.partner"]._preserve_not_env_managed_data(["field_not_a_column"])

    def test_preserve_does_not_leak_into_env_configured_field(self):
        """Keep reading from the environment when a config key is defined.

        When a config key is defined, the field must keep reading from
        the environment, regardless of any raw column value.
        """
        self._set_raw_city_column("Legacy Raw City")
        with self.load_config(public="[partner]\ncity = From Env\n"):
            self.env["res.partner"]._preserve_not_env_managed_data(["city"])
            self.partner.invalidate_recordset()
            self.assertEqual(self.partner.city, "From Env")
