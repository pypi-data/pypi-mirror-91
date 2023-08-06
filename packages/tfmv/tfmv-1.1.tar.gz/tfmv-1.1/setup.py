import os
import sys

import pipfile
from setuptools import setup, find_packages

##########
# version
##########

try:
    with open(os.path.join(os.path.dirname(__file__), 'version.txt'), 'r') as file:
        VERSION = "".join(file.readlines()).strip()
except IOError:
    VERSION = None
VERSION = os.environ.get('VERSION', VERSION)  # use environment variable if present (overrides file)
if VERSION is None:
    print("version is not specified! use 'version.txt' file at project root, or environment variable VERSION")
    sys.exit(1)


##########
# setup
##########

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

INSTALL_REQUIRES = pipfile.load('Pipfile').data['default'].keys()

setup(
    name="tfmv",
    version=VERSION,
    author='Vincent Pfister',
    author_email='vincent.pfister@raisepartner.com',
    description='Simple tool for moving / renaming resources in one or several terraform configurations.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://gitlab.raisepartner.com/it_group/infra/terraform/tfmv",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    entry_points="""
        [console_scripts]
        tfmv=tfmv.main:mv
    """
)
