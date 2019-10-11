import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-server-env",
    description="Meta package for oca-server-env Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-server_environment',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
