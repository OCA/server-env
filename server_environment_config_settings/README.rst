.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Server Environment Config Settings
==================================

Override res.config.settings from server environment file.
Before using this module, you must be familiar with the
server_environment module.

Installation
============

There is no specific installation instruction for this module.

Configuration
=============

To configure this module, you need to add a section ``[res.config.settings]`` to
you server_environment_files configurations, where the key should match the field
definition on `res.config.settings` model.

Moreover, you have to add a dependency on server_environment_files module, to
the module where the field is defined.

When the wizard is called, fields will be automatically filled with the value
defined in server_environment_files.

For example you want to change `auth_oauth_google_client_id` defined in
*auth_oauth* module:

.. code::

   [res.config.settings]
   auth_oauth_google_client_id=dummy_key_for_google_oauth


Then you should add in __manifest__.py:

.. code::

    'depends': ['base', *'auth_oauth'*]


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/149/11.0

Known issues / Roadmap
======================

* Admin user has to execute the wizard for the values to be stored in the database.
* Not tested for group_* and module_* fields

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/server-tools/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Akim Juillerat <akim.juillerat@camptocamp.com>

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
