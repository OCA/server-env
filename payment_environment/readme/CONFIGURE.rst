With this module installed, the payment acquirers are configured in
the `server_environment_files` module (which is a module you should provide,
see the documentation of `server_environment` for more information).

In the configuration file of each environment, for each payment acquirer you
may use the section `[payment_acquirer.technical_name]` to configure the
acquirer values, where "technical_name" is the acquirer's `tech_name`.

This module alone only lets you configure the `state` field, which allows to
set the acquirer's environment. Most payment acquirers will define specific
fields to store their credentials, so glue modules are required to include them
in `_server_env_fields` if that's what you want.

Example of config file ::

  [payment_acquirer.paypal]
  state = test
