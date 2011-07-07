from factory import Factory, LazyAttribute
from ftb.models import Patient, PatientDetails, Address, FamilyHistory

class CreateRelatedMixin(object):

    @classmethod
    def create_related(cls, **kwargs):
        from json import model_factory
        obj = cls.create(**kwargs)
        for related_object in cls.__dict__['_associated_class']._meta.get_all_related_objects():
            related_factory = getattr(model_factory, related_object.model.__name__ + 'Factory')
            getattr(related_factory, 'create_related' if CreateRelatedMixin in related_factory.__bases__ else 'create')(**{related_object.field.name: obj})
        return obj
    
class PatientFactory(Factory, CreateRelatedMixin):
    FACTORY_FOR = Patient
    name = 'DeepanS'

class PatientDetailsFactory(Factory):
    FACTORY_FOR = PatientDetails
    ethnic_group = 'Hindu'
    age = 29
    sex = 'M'
    visual_loss_age = 99
    patient = LazyAttribute(lambda a: PatientFactory())
    
class AddressFactory(Factory):
    FACTORY_FOR = Address
    town = 'Neyveli'
    patient = LazyAttribute(lambda a: PatientFactory())
    
class FamilyHistoryFactory(Factory):
    FACTORY_FOR = FamilyHistory
    has_family_history = True
    affected_relation = 'Uncle'
    consanguinity = False
    patient = LazyAttribute(lambda a: PatientFactory())
