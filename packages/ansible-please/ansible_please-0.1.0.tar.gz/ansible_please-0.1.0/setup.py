#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'ansible-runner', 'ansible', 'attrs', 'loguru', 'omegaconf']

setup_requirements = [ ]

test_requirements = ['docker']

setup(
    author="Shyam Sudhakaran",
    author_email='shyamsn97@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Helper package to make running Ansible a bit smoother",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='ansible_please',
    name='ansible_please',
    packages=find_packages(include=['ansible_please', 'ansible_please.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/shyamsn97/ansible_please',
    version='0.1.0',
    zip_safe=False,
)
