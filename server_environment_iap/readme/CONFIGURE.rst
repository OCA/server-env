To configure this module, you need to add a section ``[iap.account]`` to
you server_environment_files configurations, where the keys are service names
as would normally be set in the Technical / IAP Accounts Odoo menu.

When first using a value, the system will read it from the server environment file
and override any value that would be present in the database, so the server environment file has precedence.

When creating or modifying values that are in the server environment file, the
module replace changes, enforcing the configuration value.

For example you can use this module like that:

.. code::

   [iap.account]
   partner_autocomplete=secret_token
