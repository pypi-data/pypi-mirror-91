# SPDX-License-Identifier: GPL-2.0+

import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as fd:
    README = fd.read()


def get_project_version(version_file='waiverdb/__init__.py'):
    """
    Read the declared version of the project from the source code.

    Args:
        version_file: The file with the version string in it. The version must
            be in the format ``__version__ = '<version>'`` and the file must be
            UTF-8 encoded.
    """
    with open(version_file, 'r') as f:
        version_pattern = "^__version__ = '(.+)'$"
        match = re.search(version_pattern, f.read(), re.MULTILINE)
    if match is None:
        err_msg = 'No line matching %r found in %r'
        raise ValueError(err_msg % (version_pattern, version_file))
    return match.group(1)


setup(name='waiverdb',
      version=get_project_version(),
      description='An engine for storing waivers against test results.',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Red Hat, Inc.',
      author_email='qa-devel@lists.fedoraproject.org',
      license='GPLv2+',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      entry_points={
          'console_scripts': ['waiverdb-cli=waiverdb.cli:cli',
                              'waiverdb=waiverdb.manage:cli'],
      },
)
