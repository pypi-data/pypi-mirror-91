# importing setup from setuptools
from setuptools import find_packages, setup

# example to pull all data from README into var long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name = "dans-netbox-plugins",
	version = "0.57",
	description = "creating example and Pilot\"s first plugin",
    long_description = long_description,
	url = "https://github.com/dmurphy112/public",
	author = "daniel murphy",
    author_email = "dev@danielmurphy.email",
	license = "Apache 2.0",
	install_requires = [],
	packages = find_packages(),
	include_package_data = True,
	zip_safe = False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',)
