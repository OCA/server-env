The configuration file needs to edited, to add:

* ``running_env=test``: to set the environment to use, ``test`` in this example.
* ``encryption_key_test=xxxx``: to set the encryption key to use for a particular environment, ``test`` in this case.

If no encryption key is set, the User Interface will suggest one when trying to save encrypted data.

The data written in an ancrypted field is stored in a dedicated Model,
``encryted.data``, that also holds the logic to encrypt and decrypt data.

Separate values are stored for each environment.
This means that if we set value "X" on the test environment,
this value will only be available when the test environment is the active one.
