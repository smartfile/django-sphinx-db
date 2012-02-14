from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.base import DatabaseOperations as MySQLDatabaseOperations


class DatabaseOperations(MySQLDatabaseOperations):
    compiler_module = "django_sphinx.backend.sphinx.compiler"


class DatabaseWrapper(MySQLDatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.ops = DatabaseOperations()

