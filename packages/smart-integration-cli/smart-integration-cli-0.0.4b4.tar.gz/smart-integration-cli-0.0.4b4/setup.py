from setuptools import setup, find_packages

setup(
    name='smart-integration-cli',
    version='0.0.4b4',
    packages=find_packages(),
    py_modules=['smart_integration_cli', '/smart_cli', '/smart_cli/generators'],
    install_requires=['Click>=5.1', 'Jinja2>=2.10.3', 'simple-color-print',],
    entry_points="""
        [console_scripts]
        integration=smart_integration_cli:cli
    """,
    include_package_data=True,
    author='bzdvdn',
    author_email='bzdv.dn@gmail.com',
    url='https://github.com/bzdvdn/integration_cli',
)
