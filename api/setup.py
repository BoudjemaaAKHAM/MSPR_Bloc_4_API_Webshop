from setuptools import setup, find_packages

setup(
    name='api',
    version='1.0.0',
    description='API',
    author='seb',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['termcolor']
)
