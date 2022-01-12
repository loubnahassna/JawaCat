# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in jawacat/__init__.py
from jawacat import __version__ as version

setup(
	name="jawacat",
	version=version,
	description="jawacat",
	author="Maysaa Elsafadi",
	author_email="mesa_safd@hotmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
