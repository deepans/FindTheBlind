from django.db import models
from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
from ftb.exceptions import StaleObjectException

class ConcurrencyManager(models.Manager):

    def update(self, model):
        fields = model_to_dict(model,
                               fields=[field.name for field in model._meta.fields],
                               exclude=['version'])
            
            
        if self.get_query_set().filter(Q(id=model.id) &
                                       Q(version=model.version)).update(version=model.version + 1,
                                                                        **dict(fields)):
            model.version += 1
        else:
            raise StaleObjectException('Error on updating table {0} and row {1}'.format(model._meta.db_table,
                                                                                        model.__dict__['id']))
            
    
        