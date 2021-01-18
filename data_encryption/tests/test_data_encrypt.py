# © 2016 Akretion Raphaël REVERDY
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.exceptions import AccessError, ValidationError
from odoo.tools.config import config

from .common import CommonDataEncrypted

_logger = logging.getLogger(__name__)

try:
    from cryptography.fernet import Fernet
except ImportError as err:  # pragma: no cover
    _logger.debug(err)


class TestDataEncrypted(CommonDataEncrypted):
    def test_store_data_no_superuser(self):
        # only superuser can use this model
        admin = self.env.ref("base.user_admin")
        with self.assertRaises(AccessError):
            self.encrypted_data.with_user(admin.id)._encrypted_store(
                self.crypted_data_name, "My config"
            )

    def test_store_data_noenv_set(self):
        config.pop("running_env", None)
        with self.assertRaises(ValidationError):
            self.encrypted_data.sudo()._encrypted_store(
                self.crypted_data_name, "My config"
            )

    def test_store_data_nokey_set(self):
        config.pop("encryption_key_test", None)
        with self.assertRaises(ValidationError):
            self.encrypted_data.sudo()._encrypted_store(
                self.crypted_data_name, "My config"
            )

    def test_get_data_decrypted_and_cache(self):
        self.encrypted_data.sudo()._encrypted_store("test_model,1", "My config")
        data = self.encrypted_data.sudo()._encrypted_get(self.crypted_data_name)
        self.assertEqual(data, "My config")

        # Test cache really depends on user (super user) else any user could
        # access the data
        admin = self.env.ref("base.user_admin")
        with self.assertRaises(AccessError):
            self.encrypted_data.with_user(admin)._encrypted_get(self.crypted_data_name)

        # Change value should invalidate cache
        self.encrypted_data.sudo()._encrypted_store("test_model,1", "Other Config")
        new_data = self.encrypted_data.sudo()._encrypted_get(self.crypted_data_name)
        self.assertEqual(new_data, "Other Config")

    def test_get_data_wrong_key(self):
        self.encrypted_data.sudo()._encrypted_store("test_model,1", "My config")
        new_key = Fernet.generate_key()
        config["encryption_key_test"] = new_key.decode()
        with self.assertRaises(ValidationError):
            self.encrypted_data.sudo()._encrypted_get(self.crypted_data_name)

    def test_get_empty_data(self):
        empty_data = self.encrypted_data.sudo()._encrypted_get(self.crypted_data_name)
        self.assertEqual(empty_data, None)

    def test_get_wrong_json(self):
        self.encrypted_data.sudo()._encrypted_store(self.crypted_data_name, "config")
        with self.assertRaises(ValidationError):
            self.encrypted_data.sudo()._encrypted_read_json(self.crypted_data_name)

    def test_get_good_json(self):
        self.encrypted_data.sudo()._encrypted_store_json(
            self.crypted_data_name, {"key": "value"}
        )
        data = self.encrypted_data.sudo()._encrypted_read_json(self.crypted_data_name)
        self.assertEqual(data, {"key": "value"})

    def test_get_empty_json(self):
        data = self.encrypted_data.sudo()._encrypted_read_json(self.crypted_data_name)
        self.assertEqual(data, {})

    def test_get_data_with_bin_size_context(self):
        self.encrypted_data.sudo()._encrypted_store(self.crypted_data_name, "test")
        data = (
            self.encrypted_data.sudo()
            .with_context(bin_size=True)
            ._encrypted_get(self.crypted_data_name)
        )
        self.assertEqual(data, "test")
