#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

# the name of the project
name = 'nbformat'

#-----------------------------------------------------------------------------
# Minimal Python version sanity check
#-----------------------------------------------------------------------------

import sys

#-----------------------------------------------------------------------------
# get on with it
#-----------------------------------------------------------------------------

import os
from glob import glob

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))
pkg_root = pjoin(here, name)

packages = []
for d, _, _ in os.walk(pjoin(here, name)):
    if os.path.exists(pjoin(d, '__init__.py')):
        packages.append(d[len(here)+1:].replace(os.path.sep, '.'))

package_data = {
    'nbformat' : [
        'corpus/*.txt'
        'tests/*.ipynb',
        'v3/nbformat.v3*.schema.json',
        'v4/nbformat.v4*.schema.json',
    ],
}

version_ns = {}
with open(pjoin(here, name, '_version.py')) as f:
    exec(f.read(), {}, version_ns)


setup_args = dict(
    name            = name,
    version         = version_ns['__version__'],
    scripts         = glob(pjoin('scripts', '*')),
    packages        = packages,
    package_data    = package_data,
    include_package_data = True,
    description     = "The Jupyter Notebook format",
    long_description= """
    This package contains the base implementation of the Jupyter Notebook format,
    and Python APIs for working with notebooks.
    """,
    author          = 'Jupyter Development Team',
    author_email    = 'jupyter@googlegroups.com',
    url             = 'http://jupyter.org',
    license         = 'BSD',
    python_requires = '>=3.5',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Interactive', 'Interpreter', 'Shell', 'Web'],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

if 'develop' in sys.argv or any(a.startswith('bdist') for a in sys.argv):
    import setuptools

setuptools_args = {}
install_requires = setuptools_args['install_requires'] = [
    'ipython_genutils',
    'traitlets>=4.1',
    'jsonschema>=2.4,!=2.5.0',
    'jupyter_core',
]

extras_require = setuptools_args['extras_require'] = {
    'fast': ['fastjsonschema'],
    'test': ['check-manifest', 'fastjsonschema', 'testpath', 'pytest', 'pytest-cov'],
}

if 'setuptools' in sys.modules:
    setup_args.update(setuptools_args)
    setup_args['entry_points'] = {
        'console_scripts': [
            'jupyter-trust = nbformat.sign:TrustNotebookApp.launch_instance',
        ]
    }
    setup_args.pop('scripts', None)

if __name__ == '__main__':
    setup(**setup_args)
