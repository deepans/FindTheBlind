from django.db.models import AutoField
from django.db import backend, connection

def set_sequence(models):
    # postgresql: reset sequence
    for model in models:
        cursor = connection.cursor()
        autofields = [field for field in model._meta.fields if isinstance(field, AutoField)]
        
        for f in autofields:
            seq = backend.DatabaseOperations(connection).quote_name('%s_%s_seq' % (model._meta.db_table, f.name))
            cursor.execute("SELECT count(%s) from %s;" % (f.name, model._meta.db_table))
            nb = cursor.fetchall()[0][0]
            cursor.execute('ALTER SEQUENCE %s RESTART WITH %d;' % (seq, nb + 1))
