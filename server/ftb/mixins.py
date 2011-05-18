from django.db import models
from ftb.managers import ConcurrencyManager

class ConcurrentlyModifiable(models.Model):
    version = models.IntegerField('Version', default=1)

    objects = models.Manager()
    concurrency = ConcurrencyManager()

    class Meta:
        abstract = True

        
