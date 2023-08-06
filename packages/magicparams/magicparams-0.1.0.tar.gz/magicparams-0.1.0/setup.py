
from setuptools import setup, find_packages

VERSION = '0.1.0'

setup(
    name='magicparams',
    version=VERSION,
    description="Seamless and easy to use parameters manager for Machine Learning pipelines",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shudima/magicparams",
    keywords='Machine Learning',
    packages=find_packages(exclude=['test*', 'examples']),
    include_package_data=True,
)