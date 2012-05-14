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
        self.ops = SphinxOperations(self)
        self.creation = SphinxCreation(self)
        # The following can be useful for unit testing, with multiple databases
        # configured in Django, if one of them does not support transactions,
        # Django will fall back to using clear/create (instead of begin...rollback)
        # between each test. The method Django uses to detect transactions uses
        # CREATE TABLE and DROP TABLE, which ARE NOT supported by Sphinx, even though
        # transactions ARE. Therefore, we can just set this to True, and Django will
        # use transactions for clearing data between tests when all OTHER backends
        # support it.
        self.features.supports_transactions = True
