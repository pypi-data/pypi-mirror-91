# -*- coding: utf-8 -*-
from setuptools import setup
import saml2idp


with open('README.md') as readme:
    description = readme.read()


with open('HISTORY.md') as history:
    changelog = history.read()


setup(
    name='django-saml-idp',
    version=saml2idp.__version__,
    author='Gabriel de Forest, Sebastian Vetter',
    author_email='sebastian@mobify.com',
    description='SAML 2.0 IdP for Django',
    long_description='\n\n'.join([description, changelog]),
    long_description_content_type='text/markdown',
    install_requires=[
        'Django>=1.9.*',
        'M2Crypto==0.37.1',
        'beautifulsoup4>=4.7.1',
        'structlog'
    ],
    license='MIT',
    packages=['saml2idp'],
    url='http://github.com/deforestg/dj-saml-idp',
    zip_safe=False,
    include_package_data=True,
)
