#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('AUTHORS.rst') as authors_file:
    authors = authors_file.read()

with open('CHANGELOG.rst') as history_file:
    history = history_file.read()

with open('requirements_dev.txt') as test_reqs:
    test_requirements = test_reqs.read().splitlines()

requirements = [
    'numpy',
    'scipy',
    'columnar',
    'matplotlib',
    'plotly',
    'jsonschema',
    'quantify-core>=0.2.0',
    'qblox-instruments>=0.2.1',
]

setup_requirements = ['pytest-runner', ]

version = '0.2.0'

setup(
    author="The Quantify consortium consisting of Qblox and Orange Quantum Systems",
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    description="",
    install_requires=requirements,
    license="BSD-4 license",
    long_description=readme + '\n\n' + authors + '\n\n' + history,
    include_package_data=True,
    keywords='quantify-scheduler',
    name='quantify-scheduler',
    packages=find_packages(include=['quantify', 'quantify.*']),
    package_data={'': ['*.json']},  # ensures JSON schema are included
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/quantify-os/quantify-scheduler',
    version=version,
    zip_safe=False,
)
