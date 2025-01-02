from odoo.tools import config


def pre_init_hook(env):
    if config["test_enable"]:
        env["ir.mail_server"].create(
            {
                "name": "Test Outgoing Mail Server",
                "smtp_host": "localhost",
                "smtp_port": 25,
                "smtp_user": "test",
                "smtp_pass": "test123",
                "active": False,
            }
        )
        env.cr.execute(
            "SELECT * FROM ir_mail_server where name = 'Test Outgoing Mail Server'"
        )
        mail_server = env.cr.dictfetchone()
        assert mail_server
        assert mail_server["smtp_host"] == "localhost"
        assert mail_server["smtp_port"] == 25
        assert mail_server["smtp_user"] == "test"
        assert mail_server["smtp_pass"] == "test123"
        env["fetchmail.server"].create(
            {
                "name": "Test Incoming Mail Server",
                "server": "localhost",
                "port": 143,
                "user": "test",
                "password": "test123",
                "active": False,
            }
        )
        env.cr.execute(
            "SELECT * FROM fetchmail_server where name = 'Test Incoming Mail Server'"
        )
        mail_server = env.cr.dictfetchone()
        assert mail_server
        assert mail_server["server"] == "localhost"
        assert mail_server["port"] == 143
        assert mail_server["user"] == "test"
        assert mail_server["password"] == "test123"


def post_init_hook(env):
    # Migrate Outgoing Mail Server data
    env.cr.execute("SELECT * FROM ir_mail_server")
    for row in env.cr.dictfetchall():
        mail_server = (
            env["ir.mail_server"]
            .with_context(active_test=False)
            .search([("name", "=", row["name"])])
        )
        if mail_server:
            mail_server_values = {}
            for field_name, _options in env[
                "ir.mail_server"
            ]._server_env_fields.items():
                if field_name in row:
                    mail_server_values[field_name] = row[field_name]
            mail_server.update(mail_server_values)

    # Migrate Incoming Mail Server data
    env.cr.execute("SELECT * FROM fetchmail_server")
    for row in env.cr.dictfetchall():
        mail_server = (
            env["fetchmail.server"]
            .with_context(active_test=False)
            .search([("name", "=", row["name"])])
        )
        if mail_server:
            mail_server_values = {}
            for field_name, _options in env[
                "fetchmail.server"
            ]._server_env_fields.items():
                if field_name in row:
                    mail_server_values[field_name] = row[field_name]
            mail_server.update(mail_server_values)
