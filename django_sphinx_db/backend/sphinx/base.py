from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.base import DatabaseOperations as MySQLDatabaseOperations
from django.db.backends.mysql.creation import DatabaseCreation as MySQLDatabaseCreation


class SphinxOperations(MySQLDatabaseOperations):
    compiler_module = "django_sphinx_db.backend.sphinx.compiler"

    def fulltext_search_sql(self, field_name):
        return 'MATCH (%s)'


class SphinxCreation(MySQLDatabaseCreation):
    def create_test_db(self, verbosity=1, autoclobber=False):
        # NOOP, test using regular sphinx database.
        if self.connection.settings_dict['TEST_NAME']:
            test_name = self.connection.settings_dict['TEST_NAME']
            self.connection.close()
            self.connection.settings_dict['NAME'] = test_name
            cursor = self.connection.cursor()
            return test_name
        return self.connection.settings_dict['NAME']

    def destroy_test_db(self, old_database_name, verbosity=1):
        # NOOP, we created nothing, nothing to destroy.
        return


class DatabaseWrapper(MySQLDatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.ops = SphinxOperations()
        self.creation = SphinxCreation(self)
