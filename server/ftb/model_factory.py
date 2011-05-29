from factory import Factory, LazyAttribute
from ftb.models import Patient, PatientDetails, Address, FamilyHistory

class CreateRelatedMixin(object):

    @classmethod
    def create_related(cls, **kwargs):
        from ftb import model_factory
        obj = cls.create(**kwargs)
        for related_object in Patient._meta.get_all_related_objects():
            getattr(model_factory,
                    related_object.model.__name__ + 'Factory').create(**{related_object.field.name: obj})
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
