from factory import Factory, LazyAttribute
from json.tests.models import Parent, OneToOneChild, OneToManyChild, SimpleModelOne, SimpleModelTwo,\
     OneToOneParent, ReverseOneToOneChild, OneToManyParent, ReverseOneToManyChild, SimpleModelThree,\
     SimpleModelFour

class CreateRelatedMixin(object):

    @classmethod
    def create_related(cls, **kwargs):
        from json import model_factory
        obj = cls.create(**kwargs)
        for related_object in cls.__dict__['_associated_class']._meta.get_all_related_objects():
            related_factory = getattr(model_factory, related_object.model.__name__ + 'Factory')
            getattr(related_factory, 'create_related' if CreateRelatedMixin in related_factory.__bases__ else 'create')(**{related_object.field.name: obj})
        return obj

class ParentFactory(Factory, CreateRelatedMixin):
    FACTORY_FOR = Parent
    p_field1 = 'pfield1value'

class OneToOneChildFactory(Factory, CreateRelatedMixin):
    FACTORY_FOR = OneToOneChild
    o2o_field1 = 'o2ofield1value'
    o2o_field2 = 100
    o2o_field3 = 'k2'
    o2o_field4 = LazyAttribute(lambda a: ParentFactory())
    
class OneToManyChildFactory(Factory):
    FACTORY_FOR = OneToManyChild
    o2m_field1 = 'o2mfield1value'
    o2m_field2 = LazyAttribute(lambda a: OneToOneChildFactory())

class SimpleModelOneFactory(Factory):
    FACTORY_FOR = SimpleModelOne
    field1 = 'Field one'
    field2 = 100

class SimpleModelTwoFactory(Factory):
    FACTORY_FOR = SimpleModelTwo
    field1 = 'Field one value'
    field2 = 150

class ReverseOneToOneChildFactory(Factory):
    FACTORY_FOR = ReverseOneToOneChild
    field1 = 'Field 1 value'
    field2 = 199
    field3 = LazyAttribute(lambda a: OneToOneParentFactory)
    
class OneToOneParentFactory(Factory, CreateRelatedMixin):
    FACTORY_FOR = OneToOneParent
    p_field1 = 'parent field 1 value'
    o2o_child1 = LazyAttribute(lambda a: SimpleModelOneFactory())
    o2o_child2 = LazyAttribute(lambda a: SimpleModelTwoFactory())

class SimpleModelThreeFactory(Factory):
    FACTORY_FOR = SimpleModelThree
    field1 = 'Field one'
    field2 = 100

class SimpleModelFourFactory(Factory):
    FACTORY_FOR = SimpleModelFour
    field1 = 'Field one value'
    field2 = 150

class ReverseOneToManyChildFactory(Factory):
    FACTORY_FOR = ReverseOneToManyChild
    field1 = 'Field 1 value'
    field2 = 199
    field3 = LazyAttribute(lambda a: OneToManyParentFactory)
    
class OneToManyParentFactory(Factory, CreateRelatedMixin):
    FACTORY_FOR = OneToManyParent
    p_field1 = 'parent field 1 value'
    o2m_child1 = LazyAttribute(lambda a: SimpleModelThreeFactory())
    o2m_child2 = LazyAttribute(lambda a: SimpleModelFourFactory())
    
