This module does not need any configuration in Odoo.

The configuration is made in either server_environment_files, the environment variable or the configuration file as described in server_environment.

On top of the fields available when defining a record inheriting server.env.mixin, it is possible to add `__autocreate = {}`.
The value is a dictionary that will be passed when the record is created.
This allows setting required field values that are not made available.
The values are only used once, when the object is created. Changes are not used.

To continue the example provided by server_environment, to have this module create the record for storage_backend.my_sftp, the file would look like:

    # These variables are not odoo standard variables,
    # they are there to represent what your file could look like
    export WORKERS='8'
    export MAX_CRON_THREADS='1'
    export LOG_LEVEL=info
    export LOG_HANDLER=":INFO"
    export DB_MAXCONN=5

    # server environment options
    export SERVER_ENV_CONFIG="
    [storage_backend.my_sftp]
    __autocreate={}
    sftp_server=10.10.10.10
    sftp_login=foo
    sftp_port=22200
    directory_path=Odoo
    "

Another example, using a value in the creation dictionnary, when using [fs_storage](https://github.com/OCA/storage/tree/17.0/fs_storage) module, the name of the storage is required so the configuration would look like:

```ini
[fs_storage.my_sftp]
__autocreate = {"name": "My SFTP"}
protocol=sftp
options={"host": "10.10.10.10", "username": "foo", "password": "xxxxxxxxx"}
```

When the module creates such a record, it will add an xml id in the form `__server_environment_autocreate__.<section name with space replaced by ->`.

When the module is removed, the created record are kept.
They can be found by searching the xmlid for the pseudo module `__server_environment_autocreate__`.

If the creation fails with an exception, or if the values dictionary is incorrect, this will prevent the loading of the
registry. This is intended, so that odoo does not start without the intended configuration.
