import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-server-env",
    description="Meta package for oca-server-env Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-data_encryption>=16.0dev,<16.1dev',
        'odoo-addon-mail_environment>=16.0dev,<16.1dev',
        'odoo-addon-server_environment>=16.0dev,<16.1dev',
        'odoo-addon-server_environment_data_encryption>=16.0dev,<16.1dev',
        'odoo-addon-server_environment_ir_config_parameter>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
