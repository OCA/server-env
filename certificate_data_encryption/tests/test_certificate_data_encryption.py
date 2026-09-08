# Copyright (C) 2026 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import datetime

from cryptography import x509
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase
from odoo.tools.config import config


def _generate_pkcs12(password, common_name="Test Certificate"):
    """Build a base64 encoded PKCS12 archive protected by ``password``."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=365))
        .sign(key, hashes.SHA256())
    )
    p12 = pkcs12.serialize_key_and_certificates(
        name=b"test",
        key=key,
        cert=cert,
        cas=None,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode()),
    )
    return base64.b64encode(p12)


class TestCertificateDataEncryption(TransactionCase):
    """Check certificate passwords are stored encrypted per environment."""

    def setUp(self):
        super().setUp()
        self._old_running_env = config.get("running_env", "")
        self._old_keys = {
            key: config.get(key, "")
            for key in ("encryption_key_test", "encryption_key_prod")
        }
        config["running_env"] = "test"
        config["encryption_key_test"] = Fernet.generate_key().decode()
        config["encryption_key_prod"] = Fernet.generate_key().decode()

    def tearDown(self):
        config["running_env"] = self._old_running_env
        for key, value in self._old_keys.items():
            config[key] = value
        return super().tearDown()

    def _create_certificate(self, password="secret-password", **kwargs):
        vals = {
            "name": "Test Certificate",
            "content": _generate_pkcs12(password),
            "pkcs12_password": password,
        }
        vals.update(kwargs)
        return self.env["certificate.certificate"].create(vals)

    def test_password_not_stored_in_certificate_table(self):
        cert = self._create_certificate()
        self.env.cr.execute(
            "SELECT pkcs12_password FROM certificate_certificate WHERE id = %s",
            (cert.id,),
        )
        self.assertFalse(self.env.cr.fetchone()[0])
        # but still readable for the running (test) environment
        self.assertEqual(cert.pkcs12_password, "secret-password")
        # and the certificate data could be extracted from the file
        self.assertTrue(cert.pem_certificate)
        self.assertFalse(cert.loading_error)

    def test_password_stored_encrypted_in_encrypted_data(self):
        cert = self._create_certificate()
        encrypted = (
            self.env["encrypted.data"]
            .sudo()
            .search(
                [
                    ("name", "=", f"certificate.certificate,{cert.id}"),
                    ("environment", "=", "test"),
                ]
            )
        )
        self.assertTrue(encrypted)
        # the Fernet blob must not contain the clear password
        self.assertNotIn(b"secret-password", encrypted.encrypted_data)

    def test_password_is_per_environment(self):
        cert = self._create_certificate()
        # no value defined for the prod environment yet
        self.assertFalse(cert.with_context(environment="prod").pkcs12_password)
        # define the prod value from the running environment. As the
        # content is shared between environments, the password must be
        # consistent with it; the point of storing it per environment is
        # that a copy of the database without the encryption key of an
        # environment cannot read its value.
        cert.with_context(environment="prod").write(
            {"pkcs12_password": "secret-password"}
        )
        self.assertEqual(
            cert.with_context(environment="prod").pkcs12_password,
            "secret-password",
        )
        # the test environment value is unchanged and stays readable
        self.assertEqual(cert.pkcs12_password, "secret-password")
        # one encrypted row per environment
        encrypted = (
            self.env["encrypted.data"]
            .sudo()
            .search([("name", "=", f"certificate.certificate,{cert.id}")])
        )
        self.assertEqual(len(encrypted), 2)
        self.assertEqual({rec.environment for rec in encrypted}, {"test", "prod"})
        for rec in encrypted:
            self.assertNotIn(b"secret-password", rec.encrypted_data)
        # still nothing in the certificate table
        self.env.cr.execute(
            "SELECT pkcs12_password FROM certificate_certificate WHERE id = %s",
            (cert.id,),
        )
        self.assertFalse(self.env.cr.fetchone()[0])

    def test_password_is_validated_per_environment(self):
        cert = self._create_certificate()
        # writing a password inconsistent with the content for another
        # environment is rejected, even if the current environment value
        # is valid
        with self.assertRaises(ValidationError):
            cert.with_context(environment="prod").write(
                {"pkcs12_password": "prod-password"}
            )

    def test_certificate_wrong_password(self):
        with self.assertRaises(ValidationError):
            self.env["certificate.certificate"].create(
                {
                    "name": "Broken Certificate",
                    "content": _generate_pkcs12("secret-password"),
                    "pkcs12_password": "wrong-password",
                }
            )

    @staticmethod
    def _generate_encrypted_pem_key(password):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                password.encode()
            ),
        )
        return base64.b64encode(pem)

    def test_key_password_encrypted(self):
        key = self.env["certificate.key"].create(
            {
                "name": "Test Key",
                "content": self._generate_encrypted_pem_key("key-secret"),
                "password": "key-secret",
            }
        )
        self.assertTrue(key.pem_key)
        self.assertFalse(key.loading_error)
        self.env.cr.execute(
            "SELECT password FROM certificate_key WHERE id = %s", (key.id,)
        )
        self.assertFalse(self.env.cr.fetchone()[0])
        # readable from the running environment
        self.assertEqual(key.password, "key-secret")
        # and stored encrypted in the encrypted data store
        encrypted = (
            self.env["encrypted.data"]
            .sudo()
            .search(
                [
                    ("name", "=", f"certificate.key,{key.id}"),
                    ("environment", "=", "test"),
                ]
            )
        )
        self.assertTrue(encrypted)
        self.assertNotIn(b"key-secret", encrypted.encrypted_data)
