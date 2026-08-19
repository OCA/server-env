You can include a mixin in your model and configure the env-computed
fields by an override of `_server_env_fields`.

    class StorageBackend(models.Model):
        _name = "storage.backend"
        _inherit = ["storage.backend", "server.env.mixin"]

        @property
        def _server_env_fields(self):
            return {"directory_path": {}}

Read the documentation of the class and methods in
[models/server_env_mixin.py](models/server_env_mixin.py).

If you want to have a technical name to reference:

    class StorageBackend(models.Model):
        _name = "storage.backend"
        _inherit = ["storage.backend", "server.env.techname.mixin"]

        [...]

## Restoring columns on uninstall

When `server.env.mixin` is bound to an existing model, the ORM drops the
original stored columns for all env-managed fields. If the binding addon is
later uninstalled, those columns must be recreated so the database remains
usable.

Add an `uninstall_hook` to your addon and delegate to
`restore_env_managed_columns`:

    # your_addon/__init__.py
    from ./hooks import uninstall_hook
    # your_addon/hooks.py
    from odoo.addons.server_environment import uninstall

    def uninstall_hook(env):
        uninstall.restore_env_managed_columns(
            env,
            "storage.backend",
            ["directory_path", "other_field"],
        )

    # your_addon/__manifest__.py
    {
        ...
        "uninstall_hook": "uninstall_hook",
    }

The helper creates any missing columns (idempotent: safe to call multiple
times) and repopulates them with each record's current effective value —
whether that value came from an environment configuration file or from the
stored default field (`x_<field>_env_default`).

The hook must run *before* the ORM extensions are removed, which is guaranteed
by Odoo's uninstall sequence (hooks execute before `Module.module_uninstall()`).

### Handling required fields

If a restored column is **required** (has a `NOT NULL` constraint) but has no
effective value (missing from environment config and no default field set), the
restoration will fail with a `UserError`.

**Solution:** pass a `field_defaults` dictionary with fallback values:

    def uninstall_hook(env):
        restore_env_managed_columns(
            env,
            "ir.mail_server",
            ["smtp_host", "smtp_authentication"],
            field_defaults={
                "smtp_authentication": "login",  # fallback for required field
            },
        )

The helper will use the fallback value if provided and the computed field value
is empty. If no fallback is provided but a required field has no value, a
`UserError` is raised with instructions on how to provide a `field_defaults`
parameter.

## Migrating when dropping server_environment dependency

When refactoring an existing addon that embeds a `server.env.mixin` binding, you
may want to extract the binding into a separate *glue* addon and drop the
`server_environment` dependency from the original.  This keeps the base addon
lightweight while preserving server-environment features for those who install
the glue addon.

**Pattern:**

- **Original addon (v1)**: depends on `server_environment` and binds the mixin
  directly in model code.
- **Refactored addon (v2)**: removes `server_environment` from dependencies,
  removes the mixin binding and the related ORM model inheritance.
- **New glue addon** (optional, same version): depends on both `server_environment`
  and the original addon v2; re-adds the mixin binding in a separate module file.

**Migration checklist:**

1. In the **original addon's v2 `__manifest__.py`**:
   - Remove `"server_environment"` from `depends`.
   - Remove the model file(s) that contained the mixin binding.
   - Update `depends` to add the new glue addon *if* the base addon still needs it
     (otherwise, make the glue addon optional for users who want env-binding).

2. In the **original addon's v2 model code**:
   - Delete or simplify the model class that inherited from `server.env.mixin`.
   - If the model was only there for the binding, remove it entirely.
   - Restore the original field definitions (not as computed fields).

3. **Create a migration script** (if needed) to restore columns *during the addon
   upgrade*, before the ORM model extensions are unloaded.  Use a `@post_load`
   hook or a dedicated migration script:

       # migrations/18.0.1.0.0/post-restore-columns.py
       def migrate(cr, version):
           # Call the restoration logic while the v1 model is still active
           env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
           # If any field is required and may have no value in the environment,
           # provide a fallback via field_defaults
           restore_env_managed_columns(
               env,
               "storage.backend",
               ["directory_path", "other_field"],
               field_defaults={
                   "directory_path": "/tmp",  # fallback for required field
               },
           )

4. **Create the glue addon** with the model re-inheritance:

       # your_addon_env/__init__.py
       from . import models

       # your_addon_env/models/__init__.py
       from . import storage_backend

       # your_addon_env/models/storage_backend.py
       class StorageBackend(models.Model):
           _name = "storage.backend"
           _inherit = ["storage.backend", "server.env.mixin"]

           @property
           def _server_env_fields(self):
               return {"directory_path": {}}

       # your_addon_env/__manifest__.py
       {
           "name": "Storage Backend – Server Environment",
           "version": "18.0.1.0.0",
           "depends": ["server_environment", "storage_backend"],
           "installable": True,
       }

**Key points:**

- Column restoration must happen *during the addon upgrade* (step 3), not as an
  uninstall hook, because the original model binding is still active.
- The `restore_env_managed_columns` helper is idempotent and safe to call even
  if columns already exist.
- Users who do not need server environment features simply do *not* install the
  glue addon—the base addon continues to work with plain database columns.
- Users who do need server environment can install both the base addon (v2+) and
  the glue addon (same version) to get the binding back.
