# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase


class TestServerEnvMixinSameFieldName(ServerEnvironmentCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.public = (
            # global for all server.env.test records
            "[server_env_test]\n"
            "host=global_value\n"
            # for our server.env.test test record now
            "[server_env_test.foo]\n"
            "host=foo_value\n"
            # for our server.env.test2 test record now
            "[server_env_test2.foo]\n"
            "host=foo2_value\n"
        )
        cls.foo = cls.env['server.env.test'].create({'name': 'foo'})
        cls.foo2 = cls.env['server.env.test2'].create({
            'name': 'foo',
        })

    def test_env_computed_fields_read(self):
        """Read values from the config in env-computed fields"""
        with self.load_config(self.public):
            self.assertEqual(self.foo.name, 'foo')
            self.assertEqual(self.foo2.name, 'foo')
            self.assertEqual(self.foo.host, 'foo_value')
            self.assertEqual(self.foo2.host, 'foo2_value')

    def test_env_computed_fields_not_editable(self):
        """Env-computed fields without key in config can be written"""
        # we can create the record even if we didn't provide
        # the field host which was required
        with self.load_config(self.public):
            self.assertEqual(self.foo.host, 'foo_value')
            self.assertFalse(self.foo.host_env_is_editable)
            self.assertEqual(self.foo2.host, 'foo2_value')
            self.assertFalse(self.foo2.host_env_is_editable)

    def test_env_computed_fields_editable(self):
        """Env-computed fields without key in config can be written"""
        # we can create the record even if we didn't provide
        # the field host which was required
        with self.load_config():
            self.assertFalse(self.foo.host)
            self.assertTrue(self.foo.host_env_is_editable)
            self.assertFalse(self.foo2.host)
            self.assertTrue(self.foo2.host_env_is_editable)

            self.foo.host_env_default = 'foo_value'
            self.foo.invalidate_cache()
            self.assertEqual(self.foo.host, 'foo_value')

            self.foo2.host_env_default = 'foo2_value'
            self.foo2.invalidate_cache()
            self.assertEqual(self.foo2.host, 'foo2_value')

            self.foo.host = 'foo_new_value'
            self.foo.invalidate_cache()
            self.assertEqual(self.foo.host, 'foo_new_value')

            self.foo2.host = 'foo2_new_value'
            self.foo2.invalidate_cache()
            self.assertEqual(self.foo2.host, 'foo2_new_value')


class TestServerEnvMixinInherits(ServerEnvironmentCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.public = (
            # global for all server.env.test records
            "[server_env_test]\n"
            "host=global_value\n"
            # for our server.env.test test record now
            "[server_env_test.foo]\n"
            "host=foo_value\n"
            # for our server.env.test.inherits1 test record now
            "[server_env_test_inherits1.foo]\n"
            "host=foo_inherits_value\n"
            # for our server.env.test.inherits2 test record now
            "[server_env_test_inherits2.foo]\n"
            "host=foo_inherits_value\n"
        )
        cls.foo = cls.env['server.env.test'].create({'name': 'foo'})
        cls.foo_inh1 = cls.env['server.env.test.inherits1'].create({
            'name': 'foo'
        })
        cls.foo_inh2 = cls.env['server.env.test.inherits2'].create({
            'name': 'foo'
        })

    def test_env_computed_fields_read(self):
        """Read values from the config in env-computed fields"""
        with self.load_config(self.public):
            self.assertEqual(self.foo.name, 'foo')
            self.assertEqual(self.foo_inh1.name, 'foo')
            self.assertEqual(self.foo_inh2.name, 'foo')
            self.assertEqual(self.foo.host, 'foo_value')
            # inh1 does not redefine the host field so has the
            # same value than the parent record (delegate)
            self.assertEqual(self.foo_inh1.host, 'foo_value')
            # inh2 redefines self.the host field so has its own value
            self.assertEqual(self.foo_inh2.host, 'foo_inherits_value')

    def test_env_computed_fields_not_editable(self):
        """Env-computed fields without key in config can be written"""
        with self.load_config(self.public):
            self.assertEqual(self.foo.host, 'foo_value')
            self.assertFalse(self.foo.host_env_is_editable)
            self.assertEqual(self.foo_inh1.host, 'foo_value')
            self.assertFalse(self.foo_inh1.host_env_is_editable)
            self.assertEqual(self.foo_inh2.host, 'foo_inherits_value')
            self.assertFalse(self.foo_inh2.host_env_is_editable)

    def test_env_computed_fields_editable(self):
        """Env-computed fields without key in config can be written"""
        with self.load_config():
            self.assertFalse(self.foo.host)
            self.assertTrue(self.foo.host_env_is_editable)
            self.assertFalse(self.foo_inh1.host)
            self.assertTrue(self.foo_inh1.host_env_is_editable)
            self.assertFalse(self.foo_inh2.host)
            self.assertTrue(self.foo_inh2.host_env_is_editable)

            self.foo.host_env_default = 'foo_value'
            self.foo.invalidate_cache()
            self.assertEqual(self.foo.host, 'foo_value')

            self.foo.host = 'foo_new_value'
            self.foo.invalidate_cache()
            self.assertEqual(self.foo.host, 'foo_new_value')

            self.foo_inh1.host_env_default = 'foo2_value'
            self.foo_inh1.invalidate_cache()
            self.assertEqual(self.foo_inh1.host, 'foo2_value')
            self.assertEqual(self.foo_inh1.base_id.host, 'foo2_value')

            self.foo_inh1.host = 'foo2_new_value'
            self.foo_inh1.invalidate_cache()
            self.assertEqual(self.foo_inh1.host, 'foo2_new_value')
            self.assertEqual(self.foo_inh1.base_id.host, 'foo2_new_value')

            self.foo_inh2.host_env_default = 'foo_inherits_value'
            self.foo_inh2.base_id.host_env_default = 'bar_value'
            self.foo_inh2.invalidate_cache()
            self.foo_inh2.base_id.invalidate_cache()
            self.assertEqual(self.foo_inh2.host, 'foo_inherits_value')
            self.assertEqual(self.foo_inh2.base_id.host, 'bar_value')

            self.foo_inh2.host = 'foo_inherits_new_value'
            self.foo_inh2.base_id.host = 'bar_new_value'
            self.foo_inh2.invalidate_cache()
            self.foo_inh2.base_id.invalidate_cache()
            self.assertEqual(self.foo_inh2.host, 'foo_inherits_new_value')
            self.assertEqual(self.foo_inh2.base_id.host, 'bar_new_value')
