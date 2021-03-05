# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tests.common import TransactionCase
from odoo.tools.config import config

_logger = logging.getLogger(__name__)

try:
    from cryptography.fernet import Fernet
except ImportError as err:  # pragma: no cover
    _logger.debug(err)


class CommonDataEncrypted(TransactionCase):
    def setUp(self):
        super().setUp()

        self.encrypted_data = self.env["encrypted.data"]
        self.set_new_key_env("test")
        self.old_running_env = config.get("running_env", "")
        config["running_env"] = "test"
        self.crypted_data_name = "test_model,1"

    def set_new_key_env(self, environment):
        crypting_key = Fernet.generate_key()
        # The key is encoded to bytes in the module, because in real life
        # the key com from the config file and is not in a binary format.
        # So we decode here to avoid having a special behavior because of
        # the tests.
        config["encryption_key_{}".format(environment)] = crypting_key.decode()

    def tearDown(self):
        config["running_env"] = self.old_running_env
        return super().tearDown()
