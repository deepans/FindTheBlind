from factory import Factory, LazyAttribute
from json.tests.models import Parent, OneToOneChild

class CreateRelatedMixin(object):

    @classmethod
    def create_related(cls, **kwargs):
        from json import model_factory
        obj = cls.create(**kwargs)
        for related_object in cls.__dict__['_associated_class']._meta.get_all_related_objects():
            getattr(model_factory,
                    related_object.model.__name__ + 'Factory').create(**{related_object.field.name: obj})
        return obj

class ParentFactory(Factory, CreateRelatedMixin):
    FACTORY_FOR = Parent
    p_field1 = 'pfield1value'

class OneToOneChildFactory(Factory):
    FACTORY_FOR = OneToOneChild
    o2o_field1 = 'o2ofield1value'
    o2o_field2 = 100
    o2o_field3 = 'k2'
    o2o_field4 = LazyAttribute(lambda a: ParentFactory())
    
