#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'jsonpath_rw==1.4',
    'nagiosplugin==1.2.4',
    'redis==2.10.5',
    'requests==2.20.0',
]

test_requirements = [
    'bumpversion==0.5.3',
    'wheel==0.23.0',
    'watchdog==0.8.3',
    'pylint==1.5.5',
    'pytest==2.9.1',
    'pytest-cov==2.2.1',
    'pytest-mock==1.1',
    'tox==2.1.1',
    'Sphinx==1.3.1',
    'capturer==2.1.1',
    'requests_mock==0.7.0',
]

setup(
    name='temelio_monitoring',
    version='0.6.0',
    description="Temelio monitoring lib written in Python, used with Shinken.",
    long_description=readme + '\n\n' + history,
    author="Temelio",
    author_email='alexandre.chaussier@temelio.com',
    url='https://github.com/Temelio/monitoring-lib-python',
    packages=find_packages(),
    package_dir={'temelio_monitoring':
                 'temelio_monitoring'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='temelio_monitoring',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
