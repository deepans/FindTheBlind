from django.db import models
from ftb.mixins import JsonEncodable

TEST_CHOICES = (
    ('k1', 'Value1'),
    ('k2', 'Value2'),
    )

class Parent(models.Model, JsonEncodable):
    p_field1 = models.CharField('Field one')
    relations_included_in_json = ('one_to_one_relation',)

class OneToOneChild(models.Model):
    o2o_field1 = models.CharField('Field one')
    o2o_field2 = models.IntegerField('Field two')
    o2o_field3 = models.CharField('Field three', choices=TEST_CHOICES)
    o2o_field4 = models.OneToOneField(Parent, related_name='one_to_one_relation')
