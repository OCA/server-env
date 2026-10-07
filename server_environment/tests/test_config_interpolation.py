# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

import logging
import os
from unittest.mock import patch

from odoo.tools.config import config as odoo_config

from .. import server_env
from . import common

_logger = logging.getLogger(__name__)


class TestConfigInterpolation(common.ServerEnvironmentCase):
    def test_interpolation_matrix(self):
        cases = [
            ("default_default", None, None, True),
            ("default_env_true", None, "True", True),
            ("default_env_false", None, "False", False),
            ("config_true_default", "True", None, True),
            ("config_false_default", "False", None, False),
            ("config_true_env_true", "True", "True", True),
            ("config_true_env_false", "True", "False", True),
            ("config_false_env_true", "False", "True", False),
            ("config_false_env_false", "False", "False", False),
        ]

        for name, config_value, env_value, expected in cases:
            with self.subTest(name=name):
                _logger.info(name)
                self._assert_interpolation(
                    config_value,
                    env_value,
                    expected,
                )

    def _assert_interpolation(
        self,
        config_value,
        env_value,
        expected,
    ):
        config_patch = {"running_env": "testing"}

        if config_value is not None:
            config_patch["server_environment_config_interpolation"] = config_value

        env_patch = {}

        if env_value is not None:
            env_patch["SERVER_ENV_CONFIG_INTERPOLATION"] = env_value

        with (
            patch.dict(odoo_config.options, config_patch),
            patch.dict(os.environ, env_patch),
            self.set_config_dir("testfiles"),
        ):
            parser = server_env._load_config()

            val = parser.get(
                "external_service.ftp",
                "user",
            )

            if expected:
                self.assertEqual(val, "testing")
            else:
                self.assertEqual(val, "%(base_user)s")
