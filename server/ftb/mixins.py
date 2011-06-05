from django.db import models
from ftb.managers import ConcurrencyManager
from json.encoder import JsonEncoder

class ConcurrentlyModifiable(models.Model):
    version = models.IntegerField('Version', default=1)

    objects = models.Manager()
    concurrency = ConcurrencyManager()

    class Meta:
        abstract = True

class JsonEncodable(JsonEncoder):
    def json_encode(self, **options):
        if hasattr(self,'relations_included_in_json') and not options.get('relations'):
            options['relations'] = self.relations_included_in_json
        serialized_str = self.serialize([self], **options)
        #eliminate brackets in the beginning and the end
        return serialized_str[1:len(serialized_str)-1]
