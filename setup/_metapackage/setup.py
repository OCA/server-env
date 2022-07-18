import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-server-env",
    description="Meta package for oca-server-env Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-mail_environment>=15.0dev,<15.1dev',
        'odoo-addon-mail_environment_google_gmail>=15.0dev,<15.1dev',
        'odoo-addon-server_environment>=15.0dev,<15.1dev',
        'odoo-addon-server_environment_ir_config_parameter>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
