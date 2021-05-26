# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in sageimport/__init__.py
from sageimport import __version__ as version

setup(
	name='sageimport',
	version=version,
	description='Import from Sage Office Line',
	author='itsdave GmbH',
	author_email='dev@itsdave.de',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
