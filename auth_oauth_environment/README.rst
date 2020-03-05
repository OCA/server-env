.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

======================
Auth Oauth Environment
======================

This module extends the functionality of server environment to support OAuth
providers, and allows you to enable providers and set client_id key according
to environment. (Refer to module server_environment for more informations)

Installation
============

To install this module, you need to have the server_environment module
installed and properly configured.

Configuration
=============

To configure this module, you need to add a section
``[auth_oauth.provider_simple_name]`` to you server_environment_files
configurations, where 'provider_simple_name' match the simplified name field on
auth.oauth.provider.

'provider_simple_name' is the first part (until first space character) in
lower case of provider name. Using existing providers, it could be either
``google``, ``odoo.com``, or ``facebook``.

For example, if you want to activate Google and Odoo.com, your
server_environment_files should look like this ::

  [auth_oauth.google]
  enabled=True
  client_id=123456789101-abcdefghijklmnopqrstuvwxyz000000

  [auth_oauth.odoo.com]
  enabled=True


Any provider not being enabled through server_environment_files will be set as
disabled automatically.

If you want to define a new custom provider, you should pay attention to the
name to use in the server_environment_files. If you create a provider with
'Dummy auth provider' as its name, then the section should be named
``[auth_oauth.dummy]``.


Usage
=====

Once configured, Odoo will read from server_environment_files the following
fields of auth.oauth.provider :

* Allowed (``enabled``)
* Client ID (``client_id``)


Known issues / Roadmap
======================

* Due to the specific nature of this module, it cannot be tested on OCA runbot.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/server-env/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://odoo-community.org/logo.png>`_.

Contributors
------------

* Akim Juillerat <akim.juillerat@camptocamp.com>

Do not contact contributors directly about support or help with technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
