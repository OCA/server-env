To configure this module, you need to add a section
``[auth_oauth.provider_name]`` to you server_environment_files
configurations, where 'provider_name' match the tech_name field on
auth.oauth.provider.

The existing providers are ``provider_google``, ``provider_openerp`` and
``provider_facebook``. A new provider gets its tech_name from its name at
creation (``My Corp SSO`` becomes ``my_corp_sso``); renaming it afterwards
keeps the tech_name, which can be changed on the provider form.

For example, if you want to activate Google and Odoo.com, your
server_environment_files should look like this:
```
  [auth_oauth.provider_google]
  client_id=123456789101-abcdefghijklmnopqrstuvwxyz000000
  enabled=True

  [auth_oauth.provider_openerp]
  enabled=True
```

On install, providers keep the client ID and Allowed values they had, unless
server_environment_files sets them.

If you want to define a new custom provider, you should pay attention to the
tech name to use in the server_environment_files. If you create a provider with
'provider_dummy' as its tech_name, then the section should be named
``[auth_oauth.provider_dummy]``.
