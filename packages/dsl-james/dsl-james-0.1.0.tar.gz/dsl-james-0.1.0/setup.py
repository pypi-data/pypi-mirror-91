#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

from james import __version__


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'loguru', 'flake8', 'flake8-docstrings']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Robert van Straalen",
    author_email='robert.vanstraalen@datasciencelab.nl',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="CLI tool for starting up a project",
    entry_points={
        'console_scripts': [
            'james=james.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=['project', 'startup', 'cookiecutter', 'MLOps', 'cli'],
    name='dsl-james',
    packages=find_packages(include=['james', 'james.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/data-science-lab-amsterdam/james',
    version=__version__,
    zip_safe=False,
)
