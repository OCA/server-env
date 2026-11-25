# Copyright 2024, 2028 XCG Consulting (https://xcg-consulting.fr).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
import logging
from ast import literal_eval

from odoo import api, models  # type: ignore[import-untyped]

from odoo.addons.server_environment.server_env import serv_config

_logger = logging.getLogger(__name__)


class ServerEnvMixin(models.AbstractModel):
    """Inherited to add autocreation of records when register_hook is called."""

    _inherit = "server.env.mixin"

    _server_env_allow_autocreate: bool = True

    @api.model
    def _get_server_env_section_name(self, section_name: str) -> None | str:
        """From the full section name of the configuration, allow to get the name if
        the section matches the model.
        For example “storage_backend.my_sftp” (used in server_environement
        documentation) would return “my_sftp” on the model “storage.backend”.

        This is the inverse of :meth:`~_server_env_section_name`, so this method
        needs to be redefined when that method is changed.

        :param section_name: name of the configuration section
        :return: None if the section name does not match, the section name otherwise.
        """
        global_section_name = self._server_env_global_section_name()
        if section_name.startswith(f"{global_section_name}."):
            return section_name[len(global_section_name) + 1 :]
        return None

    def _register_hook(self):
        super()._register_hook()
        if self._server_env_allow_autocreate:
            for section in serv_config:
                name_value = self._get_server_env_section_name(section)
                if name_value is None:
                    continue
                if not serv_config[section].get("__autocreate", None):
                    continue
                domain = [(self._server_env_section_name_field, "=", name_value)]
                count = self.with_context(active_test=False).search_count(domain)
                if not count:
                    _logger.info("Automatic creation of section %s", section)
                    values = literal_eval(serv_config[section].get("__autocreate"))
                    values[self._server_env_section_name_field] = name_value
                    records = self.create([values])
                    self.env["ir.model.data"].create(
                        [
                            {
                                "name": section.replace(" ", "_"),
                                "model": self._name,
                                "module": "__server_environment_autocreate__",
                                "res_id": record.id,
                            }
                            for record in records
                        ]
                    )
