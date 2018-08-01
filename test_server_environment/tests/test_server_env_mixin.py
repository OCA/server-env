# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase


class TestServerEnvMixin(ServerEnvironmentCase):

    def test_env_computed_fields_read(self):
        """Read values from the config in env-computed fields"""
        public = (
            # global for all server.env.test records
            "[server_env_test]\n"
            "ssl=1\n"
            # for our server.env.test test record now
            "[server_env_test.foo]\n"
            "host=test.example.com\n"
            "port=21\n"
            "user=foo\n"
        )
        secret = (
            "[server_env_test.foo]\n"
            "password=bar\n"
        )
        # we can create the record even if we didn't provide
        # the field host which was required
        foo = self.env['server.env.test'].create({
            'name': 'foo',
        })
        with self.load_config(public, secret):
            self.assertEqual(foo.name, 'foo')
            self.assertEqual(foo.host, 'test.example.com')
            self.assertEqual(foo.port, 21)
            self.assertEqual(foo.user, 'foo')
            self.assertEqual(foo.password, 'bar')
            self.assertTrue(foo.ssl)

    def test_env_computed_fields_read_multi(self):
        """Read values in env-computed fields on several records"""
        public = (
            "[server_env_test]\n"
            "host=test.example.com\n"
            "port=21\n"
            "user=foo\n"
        )
        # we can create the record even if we didn't provide
        # the field host which was required
        foo = self.env['server.env.test'].create({
            'name': 'foo',
        })
        foo2 = self.env['server.env.test'].create({
            'name': 'foo2',
        })
        foos = foo + foo2
        with self.load_config(public):
            foos._compute_server_env()

    def test_env_computed_fields_write(self):
        """Env-computed fields without key in config can be written"""
        public = (
            # for our server.env.test test record now
            "[server_env_test.foo]\n"
            "host=test.example.com\n"
            "port=21\n"
        )
        secret = (
            "[server_env_test.foo]\n"
            "password=bar\n"
        )
        # we can create the record even if we didn't provide
        # the field host which was required
        foo = self.env['server.env.test'].create({
            'name': 'foo',
        })
        with self.load_config(public, secret):
            self.assertEqual(foo.host, 'test.example.com')
            self.assertFalse(foo.host_env_is_editable)
            self.assertEqual(foo.port, 21)
            self.assertFalse(foo.port_env_is_editable)
            self.assertEqual(foo.password, 'bar')
            self.assertFalse(foo.password_env_is_editable)

            self.assertFalse(foo.user)
            self.assertTrue(foo.user_env_is_editable)
            self.assertFalse(foo.ssl)
            self.assertTrue(foo.ssl_env_is_editable)

            # field set in config, no effect
            foo.host = 'new.example.com'
            self.assertFalse(foo.host_env_default)

            # fields not set in config, written
            foo.user = 'dummy'
            self.assertEqual(foo.user_env_default, 'dummy')
            foo.ssl = True
            self.assertTrue(foo.ssl_env_default)

    def test_env_computed_default(self):
        """Env-computed fields read from default fields"""
        # we can create the record even if we didn't provide
        # the field host which was required
        foo = self.env['server.env.test'].create({
            'name': 'foo',
        })
        # empty files
        with self.load_config():
            self.assertFalse(foo.host)
            self.assertFalse(foo.port)
            self.assertFalse(foo.password)
            self.assertFalse(foo.user)
            self.assertFalse(foo.ssl)

            self.assertTrue(foo.host_env_is_editable)
            self.assertTrue(foo.port_env_is_editable)
            self.assertTrue(foo.password_env_is_editable)
            self.assertTrue(foo.user_env_is_editable)
            self.assertTrue(foo.ssl_env_is_editable)

            foo.write({
                'host_env_default': 'test.example.com',
                'port_env_default': 21,
                'password_env_default': 'bar',
                'user_env_default': 'foo',
                'ssl_env_default': True,
            })

            # refresh env-computed fields, it should read from
            # the default fields
            foo.invalidate_cache()
            self.assertEqual(foo.host, 'test.example.com')
            self.assertEqual(foo.port, 21)
            self.assertEqual(foo.user, 'foo')
            self.assertEqual(foo.password, 'bar')
            self.assertTrue(foo.ssl)

    def test_env_custom_compute_method(self):
        """Can customize compute/inverse methods"""
        foo = self.env['server.env.test'].create({
            'name': 'foo',
        })
        self.assertNotIn('alias_env_default', foo._fields)
        with self.load_config():
            self.assertTrue(foo.alias_env_is_editable)

            foo.alias = 'test'
            self.assertEqual(foo.alias_default, 'test')

        foo = self.env['server.env.test'].create({
            'name': 'foo_with_default',
        })
        with self.load_config():
            self.assertTrue(foo.alias_env_is_editable)

            foo.alias_default = 'new_value'
            self.assertEqual(foo.alias, 'new_value')
