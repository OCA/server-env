# Copyright (C) 2026 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class Certificate(models.Model):
    _name = "certificate.certificate"
    _inherit = ["certificate.certificate", "server.env.mixin"]

    @property
    def _server_env_fields(self):
        return {"pkcs12_password": {}}

    def _compute_server_env(self):
        # While a record is being created (e.g. when Odoo precomputes the
        # stored computed fields such as ``pem_certificate`` on a new
        # record), the encrypted value cannot be resolved yet: the
        # encrypted data store is keyed by record id. Skipping the
        # computation for new records keeps the value provided in the
        # creation values available, so the certificate data can still be
        # extracted from the file exactly like without this module.
        real_records = self.filtered(lambda r: r.id)
        return super(Certificate, real_records)._compute_server_env()

    @api.constrains("content", "pem_certificate")
    def _constrains_certificate_loaded(self):
        # The password is environment managed: it is no longer stored in
        # the table and may be written alone (e.g. to define the value of
        # another environment from the running one) or not be defined at
        # all for the current environment. Check the file consistency
        # directly from the content, as reading ``pem_certificate`` here
        # could re-trigger its computation in the middle of a create (the
        # check is done again once it is computed anyway).
        for cert in self.filtered(lambda c: c.content and c.pkcs12_password):
            content = cert.with_context(bin_size=False).content
            password = cert.pkcs12_password.encode()
            leaf_pem, _additional_pems, _format = cert._parse_certificate_content(
                content, password
            )
            if not leaf_pem:
                raise ValidationError(
                    _(
                        "This certificate could not be loaded. "
                        "Either the content or the password is erroneous."
                    )
                )


class CertificateKey(models.Model):
    _name = "certificate.key"
    _inherit = ["certificate.key", "server.env.mixin"]

    @property
    def _server_env_fields(self):
        return {"password": {}}

    def _compute_server_env(self):
        # See the comment in certificate.certificate._compute_server_env.
        real_records = self.filtered(lambda r: r.id)
        return super(CertificateKey, real_records)._compute_server_env()
