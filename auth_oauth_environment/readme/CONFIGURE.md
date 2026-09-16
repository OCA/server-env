To configure this module, you need to add a section
``[auth_oauth.provider_name]`` to you server_environment_files
configurations, where 'provider_name' match the tech_name field on
auth.oauth.provider.

'provider_name' is the first part (until first space character) in
lower case of provider name. Using existing providers, it could be either
``provider_google``, ``provider_openerp``, or ``provider_facebook``.

For example, if you want to activate Google and Odoo.com, your
server_environment_files should look like this:
```
  [auth_oauth.provider_google]
  client_id=123456789101-abcdefghijklmnopqrstuvwxyz000000
  enabled=True

  [auth_oauth.provider_openerp]
  enabled=True
```

Any provider not being enabled through server_environment_files will be set as
disabled automatically.

If you want to define a new custom provider, you should pay attention to the
tech name to use in the server_environment_files. If you create a provider with
'provider_dummy' as its tech_name, then the section should be named
``[auth_oauth.provider_dummy]``.
