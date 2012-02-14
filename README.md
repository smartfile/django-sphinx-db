A [SmartFile](http://www.smartfile.com/) Open Source project.
[Read more](http://www.smartfile.com/open-source.html) about how SmartFile uses and
contributes to Open Source software.

![SmartFile](http://www.smartfile.com/images/logo.jpg)

Introduction
----

This is a simple Django database backend that allows interaction with Sphinx vial SphinxQL. It is basically the default Django MySQL backend with some changes for Sphinx.

SphinxQL is a MySQL clone mode that Sphinx searchd supports. It allows you to query indexes via regular old SQL syntax. If you are using rt (real-time) indexes, you can also add and update documents in the index.

This backend is meant to be configued as a database in the Django settings.py.

This package provides a Manager class, SQLCompiler suite and supporting code to make this possible.

Usage
----

First of all, you must define a database connection in the Django configuration.

```python
# Define the connection to Sphinx
DATABASES = {
    'default': {
        # Your default database connection goes here...
    },
    # Currently, you must name this 'sphinx', as it is used in the router.
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
```

Then define a model that derives from the SphinxModel:

```python
from django_sphinx.backend.models import SphinxModel

class MyIndex(SphinxModel):
    class Meta:
        # This next bit is important, you don't want Django to manage
        # the table for this model.
        managed = False
```

Now you can start using the ORM to interact with your index.