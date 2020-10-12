# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import json
import logging

from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError
from odoo.tools import ormcache
from odoo.tools.config import config
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError as err:  # pragma: no cover
    _logger.debug(err)


class EncryptedData(models.Model):
    """Model to store encrypted data by environment (prod, preprod...)"""

    _name = "encrypted.data"
    _description = "Store any encrypted data by environment"

    name = fields.Char(required=True, readonly=True, index=True, help="Technical name")
    environment = fields.Char(
        required=True,
        index=True,
        help="Concerned Odoo environment (prod, preprod...)",
    )
    encrypted_data = fields.Binary(attachment=False)

    _sql_constraints = [
        (
            "name_environment_uniq",
            "unique (name, environment)",
            "You can not store multiple encrypted data for the same record and \
          environment",
        )
    ]

    def _decrypt_data(self, env):
        self.ensure_one()
        cipher = self._get_cipher(env)
        try:
            return cipher.decrypt(self.encrypted_data).decode()
        except InvalidToken:
            raise ValidationError(
                _(
                    "Password has been encrypted with a different "
                    "key. Unless you can recover the previous key, "
                    "this password is unreadable."
                )
            )

    @api.model
    @ormcache("self._uid", "name", "env")
    def _encrypted_get(self, name, env=None):
        if self.env.context.get("bin_size"):
            self = self.with_context(bin_size=False)
        if not self.env.su:
            raise AccessError(
                _("Encrypted data can only be read with suspended security (sudo)")
            )
        if not env:
            env = self._retrieve_env()
        encrypted_rec = self.search([("name", "=", name), ("environment", "=", env)])
        if not encrypted_rec:
            return None
        return encrypted_rec._decrypt_data(env)

    @api.model
    @ormcache("self._uid", "name", "env")
    def _encrypted_read_json(self, name, env=None):
        data = self._encrypted_get(name, env=env)
        if not data:
            return {}
        try:
            return json.loads(data)
        except (ValueError, TypeError):
            raise ValidationError(
                _("The data you are trying to read are not in a json format")
            )

    @staticmethod
    def _retrieve_env():
        """Return the current environment
        Raise if none is found
        """
        current = config.get("running_env", False)
        if not current:
            raise ValidationError(
                _(
                    "No environment found, please check your running_env "
                    "entry in your config file."
                )
            )
        return current

    @classmethod
    def _get_cipher(cls, env):
        """Return a cipher using the key of environment.
        force_env = name of the env key.
        Useful for encoding against one precise env
        """
        key_name = "encryption_key_%s" % env
        key_str = config.get(key_name)
        if not key_str:
            raise ValidationError(
                _("No '%s' entry found in config file. " "Use a key similar to: %s")
                % (key_name, Fernet.generate_key())
            )
        # key should be in bytes format
        key = key_str.encode()
        return Fernet(key)

    @api.model
    def _encrypt_data(self, data, env):
        cipher = self._get_cipher(env)
        if not isinstance(data, bytes):
            data = data.encode()
        return cipher.encrypt(data or "")

    @api.model
    def _encrypted_store(self, name, data, env=None):
        if not self.env.su:
            raise AccessError(
                _("You can only encrypt data with suspended security (sudo)")
            )
        if not env:
            env = self._retrieve_env()
        encrypted_data = self._encrypt_data(data, env)
        existing_data = self.search([("name", "=", name), ("environment", "=", env)])
        if existing_data:
            existing_data.write({"encrypted_data": encrypted_data})
        else:
            self.create(
                {"name": name, "environment": env, "encrypted_data": encrypted_data}
            )
        self._encrypted_get.clear_cache(self)
        self._encrypted_read_json.clear_cache(self)

    @api.model
    def _encrypted_store_json(self, name, json_data, env=None):
        return self._encrypted_store(name, json.dumps(json_data), env=env)
