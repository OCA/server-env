To configure this module, you need to edit the main configuration file
of your instance, and add a directive called `running_env`. Commonly
used values are 'dev', 'test', 'production':

    [options]
    running_env=dev

You also need to set the encryption key(s). The main idea is to have
different encryption keys for your different environment, to avoid the
possibility to retrieve crucial information from the production
environment in a developement environment, for instance. So, if your
running environment is 'dev':

    [options]
    encryption_key_dev=fyeMIx9XVPBBky5XZeLDxVc9dFKy7Uzas3AoyMarHPA=

In the configuration file of your production environment, you may want
to configure all your other environments encryption key. This way, from
production you can encrypt and decrypt data for all environments.

You can generate keys with `python -c 'from cryptography.fernet import
Fernet; print(Fernet.generate_key())'`.


At the moment (November 2026), odoo pins the cryptography dependency to:
```
# https://github.com/odoo/odoo/blob/18.0/requirements.txt
cryptography==3.4.8; python_version < '3.12'  # incompatibility between pyopenssl 19.0.0 and cryptography>=37.0.0
cryptography==42.0.8 ; python_version >= '3.12'  # (Noble) min 41.0.7, pinning 42.0.8 for security fixes
```

`cryptography==50.0.0` works with odoo on python3.12
`cryptography==50.0.0` does not work with odoo on python3.11
