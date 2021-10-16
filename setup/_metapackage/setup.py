import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-server-env",
    description="Meta package for oca-server-env Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-auth_oauth_environment',
        'odoo11-addon-mail_environment',
        'odoo11-addon-server_environment',
        'odoo11-addon-server_environment_files_sample',
        'odoo11-addon-server_environment_ir_config_parameter',
        'odoo11-addon-test_server_environment',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)
