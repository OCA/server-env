Follow the configuration of the ``server_environment`` and
``server_environment_data_encryption`` modules:

- define ``running_env`` in the Odoo configuration file;
- define one Fernet key per environment in the ``[options]`` section,
  e.g. ``encryption_key_prod = ZZZ``;

- generate the keys with: ``python -c 'from cryptography.fernet import
  Fernet; print(Fernet.generate_key())'``.

The passwords are **no longer stored in the** ``certificate.certificate``
and ``certificate.key`` **tables**: they are set/changed from the forms
(the screen shows which environment is being edited) and are stored
encrypted in the ``encrypted.data`` table, per environment.

If no encryption key is configured for the current environment, the
module has no effect (default behavior of
``server_environment_data_encryption``).
