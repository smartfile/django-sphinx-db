django-sphinx-db
================

Introduction
------------

This is a simple Django database backend that allows interaction with Sphinx
via SphinxQL. It is basically the default Django MySQL backend with some changes
for Sphinx.

SphinxQL is a MySQL clone mode that Sphinx searchd supports. It allows you to
query indexes via regular old SQL syntax. If you are using rt (real-time) indexes,
you can also add and update documents in the index.

This backend is meant to be configued as a database in the Django settings.py.

This package provides a Manager class, SQLCompiler suite and supporting code to
make this possible.

Usage
-----

First of all, you must define a database connection in the Django configuration.
You must also install the Sphinx database router and add django_sphinx_db to your
INSTALLED_APPS list.

::

    # Install django_sphinx_db:
    INSTALLED_APPS += ('django_sphinx_db', )

    # This is the name of the sphinx server in DATABASES:
    SPHINX_DATABASE_NAME = 'sphinx'

    # Define the connection to Sphinx
    DATABASES = {
        'default': {
            # Your default database connection goes here...
        },
        SPHINX_DATABASE_NAME:  {
            'ENGINE': 'django_sphinx_db.backend.sphinx',
            # The database name does not matter.
            'NAME': '',
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
    )    ```

Then define a model that derives from the SphinxModel. As usual, the model will be placed in models.py.

::

    from django_sphinx_db.backend.models import SphinxModel, SphinxField

    class MyIndex(SphinxModel):
        class Meta:
            # This next bit is important, you don't want Django to manage
            # the table for this model.
            managed = False

        name = SphinxField()
        content = SphinxField()
        date = models.DateTimeField()
        size = models.IntegerField()

Configuring Sphinx
------------------

Now you need to generate a configuration file for your index. A management
command is provided to convert the model definition to a suitable configuration.

::

    $ python manage.py syncsphinx >> /etc/sphinx.conf
    $ vi /etc/sphinx.conf

The generated config file should be a good start however, you are urged to
review the configuration against the
[Sphinx configuration reference](http://sphinxsearch.com/docs/2.0.2/confgroup-index.html).

Using the Django ORM with Sphinx
--------------------------------

You can now query and manage your real-time index using the Django ORM. You can
insert and update documents in the index using the following methods. The example
below uses the [fulltext library](https://github.com/btimby/fulltext) for reading
file contents as plain text.

::

    import os, time, fulltext

    # Add a document to the index.
    path = 'resume.doc'
    st = os.stat(path)
    MyIndex.objects.create(
        name = path,
        content = fulltext.get(path, ''),
        size = st.st_size,
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime)),
    )

    # Update a document in the index
    doc = MyIndex.objects.get(pk=1)
    doc.content = fulltext.get(path, '')
    doc.size = st.st_size
    doc.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime))
    doc.save()

You can perform full-text queries using the Django `search` operator. Read the
`Django documentation`_ for more information.

::

    MyIndex.objects.filter(content__search='Foobar')

The query is passed through directly to Sphinx, so the
`Sphinx extended query syntax`_
is respected.

Unit Testing
------------

The Sphinx backend for Django will ignore create_test_db and destroy_test_db calls. These
calls will fail when the Sphinx database is configured, preventing you from running tests.
However, this means that any configured Sphinx database will be used during testing. As
long as you write your tests with this in mind, there should be no problem. Remember that you
can use the TEST_NAME database connection parameter to redirect queries to a different database
connection during test runs.

.. _SmartFile: http://www.smartfile.com/
.. _Read more: http://www.smartfile.com/open-source.html
.. _Django documentation: https://docs.djangoproject.com/en/dev/ref/models/querysets/#search
.. _Sphinx extended query syntax: http://sphinxsearch.com/docs/2.0.2/extended-syntax.html
