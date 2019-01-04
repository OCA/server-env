With this module installed, the incoming and outgoing mail servers are
configured in the `server_environment_files` module (which is a module
you should provide, see the documentation of `server_environment` for
more information).

In the configuration file of each environment, you may first use the
sections `[outgoing_mail]` and `[incoming_mail]` to configure the
default values respectively for SMTP servers and the IMAP/POP servers.

Then for each server, you can define additional values or override the
default values with a section named `[outgoing_mail.resource_name]` or
`[incoming_mail.resource_name]` where "resource_name" is the name of
the server.

Example of config file ::

  [outgoing_mail]
  smtp_host = smtp.myserver.com
  smtp_port = 587
  smtp_user =
  smtp_pass =
  smtp_encryption = ssl

  [outgoing_mail.odoo_smtp_server1]
  smtp_user = odoo
  smtp_pass = odoo

  [incoming_mail.odoo_pop_mail1]
  server = mail.myserver.com
  port = 110
  type = pop
  is_ssl = 0
  attach = 0
  original = 0
  user = odoo@myserver.com
  password = uas1ohV0

You will need to create 2 records in the database, one outgoing mail
server with the field `name` set to "odoo_smtp_server1" and one
incoming mail server with the field `name` set to "odoo_pop_mail1".
