
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/server-env&target_branch=12.0)
[![Pre-commit Status](https://github.com/OCA/server-env/actions/workflows/pre-commit.yml/badge.svg?branch=12.0)](https://github.com/OCA/server-env/actions/workflows/pre-commit.yml?query=branch%3A12.0)
[![Build Status](https://github.com/OCA/server-env/actions/workflows/test.yml/badge.svg?branch=12.0)](https://github.com/OCA/server-env/actions/workflows/test.yml?query=branch%3A12.0)
[![codecov](https://codecov.io/gh/OCA/server-env/branch/12.0/graph/badge.svg)](https://codecov.io/gh/OCA/server-env)
[![Translation Status](https://translation.odoo-community.org/widgets/server-env-12-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/server-env-12-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Odoo server environment

This repository hosts official server environment management modules provided by the OCA.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[carrier_environment](carrier_environment/) | 12.0.1.0.1 |  | Configure carriers with server_environment_files
[data_encryption](data_encryption/) | 12.0.1.0.0 |  | Store accounts and credentials encrypted by environment
[mail_environment](mail_environment/) | 12.0.1.0.0 |  | Configure mail servers with server_environment_files
[pos_environment](pos_environment/) | 12.0.1.0.1 |  | Custom messages on the bill depending on the environment
[server_environment](server_environment/) | 12.0.2.0.8 |  | move some configurations out of the database
[server_environment_data_encryption](server_environment_data_encryption/) | 12.0.1.0.0 |  | Server Environment Data Encryption
[server_environment_files_sample](server_environment_files_sample/) | 12.0.1.0.1 |  | sample config file for server_environment
[server_environment_ir_config_parameter](server_environment_ir_config_parameter/) | 12.0.1.0.1 |  | Override System Parameters from server environment file

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
