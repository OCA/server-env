# Copyright 2021 Camptocamp SA <https://www.camptocamp.com/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.auth_saml.controllers.main import SAMLLogin


class SAMLLoginEnv(SAMLLogin):
    def _list_saml_providers_domain(self):
        """OVERWRITE domain to return all active IDP

        The configuration of an IDP doesn't rely anymore on
        sp_pem_public and sp_pem_private as those could be
        set through sp_pem_private_path and sp_pem_public_path.

        Keeping it simple by relying only on the active field.
        """
        return []
