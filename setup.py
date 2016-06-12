#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='temelio_monitoring',
    version='0.1.0',
    description="Temelio monitoring lib written in Python, used with Shinken.",
    long_description=readme + '\n\n' + history,
    author="Temelio",
    author_email='alexandre.chaussier@temelio.com',
    url='https://github.com/Temelio/monitoring-lib-python',
    packages=[
        'temelio_monitoring',
    ],
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
