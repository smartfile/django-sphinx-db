from django.db import models
from django.db.models.sql import Query
from django.db.models.sql.where import WhereNode
from django.db.models.query import QuerySet


class SphinxWhereNode(WhereNode):
    def sql_for_columns(self, data, qn, connection):
        table_alias, name, db_type = data
        return connection.ops.field_cast_sql(db_type) % name


class SphinxQuery(Query):
    compiler = 'SphinxQLCompiler'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('where', SphinxWhereNode)
        super(SphinxQuery, self).__init__(*args, **kwargs)


class SphinxQuerySet(QuerySet):
    def __init__(self, model, **kwargs):
        kwargs.setdefault('query', SphinxQuery(model))
        super(SphinxQuerySet, self).__init__(model, **kwargs)


class SphinxManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return SphinxQuerySet(self.model).defer('name', 'content')


class SphinxModel(models.Model):
    pass
