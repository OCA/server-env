With server_environment_data_encryption, there is nothing to configure for this module.

But, if you go with configurations files, you have to set 

- `stripe_publishable_key`
- `stripe_secret_key`
- `stripe_webhook_secret`

in the `[payment_provider.stripe]` section.
