#!/usr/bin/env python

import os

from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    readme = f.read()

requirements = ['requests', 'rx>=3.0.0']
test_requirements = ['pipenv', 'twine', 'pytest-cov', 'pytest', 'responses', 'wheel', 'tox']
setup_requirements = ['pipenv', 'setuptools']

setup(
    author='Pillar',
    author_email='opensource@pillar.gg',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='Twitch module for Python',
    install_requires=requirements,
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='Twitch API',
    name='pillar-twitch-python',
    packages=find_packages(),
    python_requires=">=3.7",
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/pillargg/Twitch-Python',
    version='0.0.20',
    zip_safe=True,
)
