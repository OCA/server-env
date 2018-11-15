import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-odoo12-addons-oca-server-env",
    description="Meta package for odoo12-addons-oca-server-env Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-server_environment',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
