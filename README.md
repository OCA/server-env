![Licence](https://img.shields.io/badge/licence-AGPL--3-blue.svg)
[![Runbot Status](https://runbot.odoo-community.org/runbot/badge/flat/254/11.0.svg)](https://runbot.odoo-community.org/runbot/repo/github-com-oca-server-env-254)
[![Build Status](https://travis-ci.org/OCA/server-env.svg?branch=11.0)](https://travis-ci.org/OCA/server-env)
[![Coverage Status](https://coveralls.io/repos/OCA/server-env/badge.svg?branch=11.0)](https://coveralls.io/r/OCA/server-env?branch=11.0)


Odoo server environment
=======================

This repository hosts official server environment managment modules provided by the OCA.

Those modules provides a way to define an environment in the main Odoo configuration file and to read some
configuration files depending on the environment you defined.

To define an environment, put 'dev', 'test', 'production' in your odoo configuration file:

```
[options]
running_env=dev
```

[//]: # (addons)

Available addons
----------------
addon | version | summary
--- | --- | ---
[mail_environment](mail_environment/) | 11.0.1.1.0 | Configure mail servers with server_environment_files
[server_environment](server_environment/) | 11.0.2.0.0 | move some configurations out of the database
[server_environment_files_sample](server_environment_files_sample/) | 11.0.1.0.0 | sample config file for server_environment
[server_environment_ir_config_parameter](server_environment_ir_config_parameter/) | 11.0.1.0.0 | Override System Parameters from server environment file
[test_server_environment](test_server_environment/) | 11.0.1.0.0 | Used to run automated tests, do not install

[//]: # (end addons)

Translation Status
------------------
[![Transifex Status](https://www.transifex.com/projects/p/OCA-server-env-11-0/chart/image_png)](https://www.transifex.com/projects/p/OCA-server-env-11-0)

----

OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.
