![Licence](https://img.shields.io/badge/licence-AGPL--3-blue.svg)
[![Runbot Status](https://runbot.odoo-community.org/runbot/badge/flat/254/12.0.svg)](https://runbot.odoo-community.org/runbot/repo/github-com-oca-server-env-254)
[![Build Status](https://travis-ci.org/OCA/server-env.svg?branch=12.0)](https://travis-ci.org/OCA/server-env)
[![Coverage Status](https://coveralls.io/repos/OCA/server-env/badge.svg?branch=12.0)](https://coveralls.io/r/OCA/server-env?branch=12.0)


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



Translation Status
------------------
[![Transifex Status](https://www.transifex.com/projects/p/OCA-server-env-12-0/chart/image_png)](https://www.transifex.com/projects/p/OCA-server-env-12-0)

----

OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.
