To configure this module, you need to:

Create a module server_environment_file with a cfg file or set the environment variable
SERVER_ENV_CONFIG with the following section:

[auth_saml_provider.<name>]

Where <name> is optional and must be equal to the name field you defined in Odoo for the IDP.


Example of configuration

[auth_saml_provider.my_idp]

idp_metadata=<...>
sp_baseurl=https://odoo-community.org
sp_pem_public_path=/data/cert.pem
sp_pem_private_path=/data/key.pem
