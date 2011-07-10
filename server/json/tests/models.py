from django.db import models
from json.mixins import JsonEncodable

TEST_CHOICES = (
    ('k1', 'Value1'),
    ('k2', 'Value2'),
    )

class Parent(models.Model, JsonEncodable):
    p_field1 = models.CharField('Field one', max_length=50)
    relations_included_in_json = {'onetoonechild': {'relations': ('onetomanychild',)}}

class OneToOneChild(models.Model):
    o2o_field1 = models.CharField('Field one', max_length=50)
    o2o_field2 = models.IntegerField('Field two')
    o2o_field3 = models.CharField('Field three', max_length=50, choices=TEST_CHOICES)
    o2o_field4 = models.OneToOneField(Parent, related_name='onetoonechild')
    
class OneToManyChild(models.Model):
    o2m_field1 = models.CharField('Field one', max_length=50)
    o2m_field2 = models.ForeignKey(OneToOneChild, related_name='onetomanychild')


class SimpleModelOne(models.Model, JsonEncodable):
    field1 = models.CharField('Field one', max_length=50)
    field2 = models.IntegerField('Field Two')

class SimpleModelTwo(models.Model, JsonEncodable):
    field1 = models.CharField('Field one', max_length=50)
    field2 = models.IntegerField('Field Two')

class OneToOneParent(models.Model, JsonEncodable):
    p_field1 = models.CharField('Field one', max_length=50)    
    o2o_child1 = models.OneToOneField(SimpleModelOne)
    o2o_child2 = models.OneToOneField(SimpleModelTwo)
    relations_included_in_json = ('o2o_child1', 'o2o_child2')

    
