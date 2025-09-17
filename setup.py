from setuptools import setup, find_packages

setup(
    name='network_cli_toolkit',
    version='1.0.0',
    packages=find_packages(),
    py_modules=['network_tool'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'netcli=network_tool:main',
        ],
    },
    author='Sohail Sajid',
    description='A CLI for working with IPs, subnets, and CIDR networking.',
    python_requires='>=3.7',
)