from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A helper package for the Imbalance project'
LONG_DESCRIPTION = 'Contains methods to connect to the datalakes and handle files'
setup(
    name='ae_python_imbalance',
    version=VERSION,
    author='Håkon Klausen',
    author_email='hakon.klausen@ae.no',
    packages=['ae_python_imbalance'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=[
        "azure.identity",
        "dotenv"
    ]
)