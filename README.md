A [SmartFile](http://www.smartfile.com/) Open Source project.
[Read more](http://www.smartfile.com/open-source.html) about how SmartFile uses and
contributes to Open Source software.

![SmartFile](http://www.smartfile.com/images/logo.jpg)

Introduction
----

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
----

First of all, you must define a database connection in the Django configuration.
You must also install the Sphinx database router and add django_sphinx to your
INSTALLED_APPS list.

```python
# Install django_sphinx:
INSTALLED_APPS += ('django_sphinx', )

# Define the connection to Sphinx
DATABASES = {
    'default': {
        # Your default database connection goes here...
    },
    'sphinx':  {
        'ENGINE': 'django_sphinx.backend.sphinx',
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
    'django_sphinx.routers.SphinxRouter',
)

# Let the router know which database is Sphinx.
SPHINX_DATABASE_NAME = 'sphinx'
```

Then define a model that derives from the SphinxModel:

```python
from django_sphinx.backend.models import SphinxModel, SphinxField

class MyIndex(SphinxModel):
    class Meta:
        # This next bit is important, you don't want Django to manage
        # the table for this model.
        managed = False

    name = SphinxField()
    content = SphinxField()
    date = models.DateTimeField()
    size = models.IntegerField()
```

Configuring Sphinx
----

Now you need to generate a configuration file for your index. A management
command is provided to convert the model definition to a suitable configuration.

```
$ python manage.py syncsphinx >> /etc/sphinx.conf
$ vi /etc/sphinx.conf
```

The generated config file should be a good start however, you are urged to
check that everything is correct. A reference can be found at the link below.

http://sphinxsearch.com/docs/2.0.2/confgroup-index.html

Using the Django ORM with Sphinx
----

You can now query and manage your real-time index using the Django ORM. You can
insert and update documents in the index using the following methods. The example
below uses the [fulltext library](https://github.com/btimby/fulltext) for reading file contents as plain text.

```python
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
```

