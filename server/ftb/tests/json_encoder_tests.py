from django.test import TestCase
from ftb.models import Patient, Address
from ftb.model_factory import PatientFactory, PatientDetailsFactory, AddressFactory, FamilyHistoryFactory

class JsonEncoderTest(TestCase):
    def test_should_encode_a_model_into_json_representation(self):
        patient = PatientFactory.create_related()
        print Patient.objects.select_related('address', 'details', 'family_history').get(id=patient.id).toJSON()
        self.assertFalse(True)
        
