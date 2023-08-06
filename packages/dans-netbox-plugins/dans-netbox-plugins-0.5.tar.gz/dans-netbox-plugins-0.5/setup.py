# interestingly the NTC example does not have a setup.py file. Creating to follow the documentation

'''
This file will be used to install the plugin.
According to the documenation, the primary purpose of this file is to call `setuptools` lib's `setup()` funct.
The `setup()` funct will create a python distribution package.

We can pass a number of kwargs to the function as well as plugin metadata.
'''

# importing setup from setuptools
from setuptools import find_packages, setup

# example to pull all data from README into var long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()




# defining python package as generic Dan's tools
'''
Since I have read up on Distutlis, we should be specifying the two packages by name, but the netbox documentation uses this `find_packages()` func. Will test out, if it does not work, I will statically spec our packages, animal_sounds and patch_tracker.
'''
setup(
	name = "dans-netbox-plugins",
	version = "0.5",
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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',)
