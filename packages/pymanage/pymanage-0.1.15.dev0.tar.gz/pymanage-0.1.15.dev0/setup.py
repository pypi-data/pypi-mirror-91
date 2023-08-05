#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

def long_description():
    description = []
    for filename in ['README.md', 'HISTORY.md']:
        with open(filename, 'r') as fd:
            description.append(fd.read())

    return '\n\n'.join(description)

requirements = ['Click>=7.0', 'PyYAML>=3.11']

test_requirements = ['pytest>=2.9.2', 'pytest-xdist>=1.14']

setup(
    name='pymanage',
    version='0.1.15-dev0',
    description="Command Line Manager + Interactive Shell for Python Projects",
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author="Bruno Rocha, Jorge Cardona",
    url='https://gitlab.com/jorgeecardona/pymanage',
    packages=['manage'],
    package_dir={'manage': 'manage'},
    entry_points={'console_scripts': ['manage=manage.cli:main']},
    include_package_data=True,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords='manage',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
