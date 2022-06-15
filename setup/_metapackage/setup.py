import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-server-env",
    description="Meta package for oca-server-env Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-auth_saml_environment',
        'odoo14-addon-data_encryption',
        'odoo14-addon-mail_environment',
        'odoo14-addon-payment_environment',
        'odoo14-addon-server_environment',
        'odoo14-addon-server_environment_data_encryption',
        'odoo14-addon-server_environment_iap',
        'odoo14-addon-server_environment_ir_config_parameter',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
