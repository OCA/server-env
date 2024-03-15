Example of config file :

    [ir.config_parameter]
    microsoft_outlook_client_id = YOUR_OFFICE365_CLIENT_ID
    microsoft_outlook_client_secret = YOUR_OFFICE365_CLIENT_SECRET

    [outgoing_mail.office365_smtp_server]
    smtp_host = smtp.office365.com
    smtp_port = 587
    smtp_user = example@yourdomain.com
    smtp_encryption = starttls
    use_microsoft_outlook_service = True

These two are global parameters, in core they're configured in General
Settings:

- \`YOUR_OFFICE365_CLIENT_ID\`: Outlook Client Id'.
- \`YOUR_OFFICE365_CLIENT_SECRET\`: Outlook Client Secret'.
