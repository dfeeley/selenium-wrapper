from distutils.core import setup

setup(
    name='selenium-wrapper',
    version='0.1',
    description='A lightweight wrapper over selenium webdriver',
    author='David Feeley',
    author_email='davidpfeeley@gmail.com',
    packages=['selenium_wrapper'],
    install_requires=['selenium'],
)
