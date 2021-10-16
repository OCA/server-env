import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-server-env",
    description="Meta package for oca-server-env Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-carrier_environment',
        'odoo12-addon-data_encryption',
        'odoo12-addon-mail_environment',
        'odoo12-addon-pos_environment',
        'odoo12-addon-server_environment',
        'odoo12-addon-server_environment_data_encryption',
        'odoo12-addon-server_environment_ir_config_parameter',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
