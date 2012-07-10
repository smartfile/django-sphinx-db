#!/bin/env python

import os
from distutils.core import setup

name = 'django_sphinx_db'
version = '0.1'
release = '1'
versrel = version + '-' + release
readme = os.path.join(os.path.dirname(__file__), 'README.rst')
download_url = 'https://github.com/downloads/btimby/django-sphinx-db' \
                           '/' + name + '-' + versrel + '.tar.gz'
long_description = file(readme).read()

setup(
    name = name,
    version = versrel,
    description = 'Django database backend for SphinxQL.',
    long_description = long_description,
    author = 'Ben Timby',
    author_email = 'btimby@gmail.com',
    maintainer = 'Ben Timby',
    maintainer_email = 'btimby@gmail.com',
    url = 'http://github.com/btimby/django-sphinx-db/',
    download_url = download_url,
    license = 'GPLv3',
    packages = [
        "django_sphinx_db",
        "django_sphinx_db.backend",
        "django_sphinx_db.backend.sphinx",
        "django_sphinx_db.management",
        "django_sphinx_db.management.commands",
    ],
    classifiers = (
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
