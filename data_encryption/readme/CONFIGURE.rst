To configure this module, you need to edit the main configuration file
of your instance, and add a directive called ``running_env``. Commonly
used values are 'dev', 'test', 'production'::

  [options]
  running_env=dev


You also need to set the encryption key(s). The main idea is to have different
encryption keys for your different environment, to avoid the possibility to retrieve
crucial information from the production environment in a developement environment, for instance.
So, if your running environment is 'dev'::

  [options]
  encryption_key_dev=fyeMIx9XVPBBky5XZeLDxVc9dFKy7Uzas3AoyMarHPA=

In the configuration file of your production environment, you may want to configure
all your other environments encryption key. This way, from production you can encrypt and decrypt
data for all environments.

You can generate keys with python -c 'from cryptography.fernet import Fernet; print Fernet.generate_key()'.
