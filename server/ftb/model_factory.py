from factory import Factory, LazyAttribute
from ftb.models import Patient, PatientDetails, Address, FamilyHistory
from datetime import date

class CreateRelatedMixin(object):

    @classmethod
    def create_related(cls, **kwargs):
        from ftb import model_factory
        obj = cls.create(**kwargs)
        for related_object in cls.__dict__['_associated_class']._meta.get_all_related_objects():
            related_factory = getattr(model_factory, related_object.model.__name__ + 'Factory')
            getattr(related_factory, 'create_related' if CreateRelatedMixin in related_factory.__bases__ else 'create')(**{related_object.field.name: obj})
        return obj
    
class PatientFactory(Factory, CreateRelatedMixin):
    FACTORY_FOR = Patient
    name = 'Arjun'

class PatientDetailsFactory(Factory):
    FACTORY_FOR = PatientDetails
    ethnic_group = 'Hindu'
    age = 29
    date_of_birth = date(2011, 1, 31)
    gender = 'M'
    fathers_name = 'Ramanan'
    fathers_phone_number = 9520012200
    mothers_name = 'Sita'
    mothers_phone_number = 9520012211
    guardians_name = 'John'
    guardians_phone_number = 9520012222
    health_workers_name = 'Ahmad'
    health_workers_phone_number = 9520012233
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
