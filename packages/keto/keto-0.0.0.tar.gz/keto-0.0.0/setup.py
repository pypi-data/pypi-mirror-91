# -*- coding=utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# keto: RPA Framework
#
# keto/setup.py
#
# Author: Dwight D. Cummings
#
# This module is part of "keto" and is released under
# mit License: http://www.opensource.org/licenses/mit
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""Called by pip. Builds and installs distributions."""


from importlib.resources import read_text
from setuptools import setup

import keto


about = {}
exec(read_text(keto, '__about__.py'), about)


def long_desc():
    try:
        with open('README.md') as f:
            return f.read()
    except OSError:
        return about.get('__summary__', about.get('__title__', ''))


setup(
    # The name that you pip/pipenv install
    # Also the name that appears in the top banner with version
    name=about['__handle__'],
    version=about['__version__'],
    # Identifies the code base by identifying the top level packages
    packages=['keto'],
    # Appears in project links
    url=about['__url__'],
    license=about['__license__'],
    # Forms the author/email tag
    author=about['__author__'],
    author_email=about['__email__'],
    # Description appears in the second grey banner
    description=about['__title__'],
    # Appears in the right pane
    long_description=long_desc(),
    long_description_content_type='text/markdown',
    # classifiers section
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ]
)
