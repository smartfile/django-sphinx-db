#!/bin/env python

from distutils.core import setup

name = 'django_sphinx_db'
version = '0.1'
release = '1'
versrel = version + '-' + release
download_url = 'https://github.com/downloads/btimby/django-sphinx-db' \
                           '/' + name + '-' + versrel + '.tar.gz'
description = """\
A `SmartFile`_ Open Source project. `Read more`_ about how SmartFile
uses and contributes to Open Source software.

.. figure:: http://www.smartfile.com/images/logo.jpg
   :alt: SmartFile

Introduction
------------

This is a simple Django database backend that allows interaction with Sphinx vial SphinxQL. It is basically the default Django MySQL backend with some changes for Sphinx.

SphinxQL is a MySQL clone mode that Sphinx searchd supports. It allows you to query indexes via regular old SQL syntax. If you are using rt (real-time) indexes, you can also add and update documents in the index.

This backend is meant to be configued as a database in the Django settings.py.

This package provides a Manager class, SQLCompiler suite and supporting code to make this possible.

Usage
-----

First of all, you must define a database connection in the Django configuration.

```python
# Define the connection to Sphinx
DATABASES = {
    'default': {
        # Your default database connection goes here...
    },
    'sphinx':  {
        'ENGINE': 'django_sphinx_db.backend.sphinx',
        # The database name does not matter.
        'NAME': 'foobar',
        # There is no user name or password.
        'USER': '',
        'PASSWORD': '',
        # Don't use localhost, this will result in using a UDS instead of TCP...
        'HOST': '127.0.0.1',
        'PORT': '9306',
    },
}

# ... and route accordingly ...
DATABASE_ROUTERS = (
    'django_sphinx_db.routers.SphinxRouter',
)

# Let the router know which database is Sphinx.
SPHINX_DATABASE_NAME = 'sphinx'
```

Then define a model that derives from the SphinxModel:

```python
from django_sphinx_db.backend.models import SphinxModel

class MyIndex(SphinxModel):
    class Meta:
        # This next bit is important, you don't want Django to manage
        # the table for this model.
        managed = False
```

Now you can start using the ORM to interact with your index.
"""


setup(
    name = name,
    version = versrel,
    description = 'Django database backend for SphinxQL.',
    long_description = description,
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
