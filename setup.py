from setuptools import setup, find_packages

setup(
    name='webshop_api',
    version='1.0.0',
    description='',
    author='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['fastapi', 'uvicorn', 'requests', 'pydantic']
)
