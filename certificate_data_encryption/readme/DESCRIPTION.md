This module allows to store the passwords of the certificates and
private keys managed by the core ``certificate`` module in an
**encrypted** and **per environment** way (dev, staging, production),
instead of clear text in the database.

It connects the core ``certificate`` module with the OCA server-env
encryption mechanism (``server_environment_data_encryption`` and
``data_encryption``): the passwords become environment managed fields
(``server.env.mixin``) whose values are stored encrypted in the
``encrypted.data`` table using a Fernet key per environment.

Covered fields:

- ``certificate.certificate.pkcs12_password``
- ``certificate.key.password``
