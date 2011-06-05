from django.test import TestCase
from ftb.models import Patient, Address
from ftb.model_factory import PatientFactory, PatientDetailsFactory, AddressFactory, FamilyHistoryFactory

class JsonEncoderTest(TestCase):
    def test_should_encode_a_model_into_json_representation(self):
        patient = PatientFactory.create_related()
        expected_json_string = '{"pk": 1, "model": "ftb.patient", "fields": {"patientdetails": {"pk": 1, "model": "ftb.patientdetails", "fields": {"patient": 1, "visual_loss_age": 99, "age": 29, "sex": "M", "ethnic_group": "Hindu", "version": 1}}, "address": {"pk": 1, "model": "ftb.address", "fields": {"town": "Neyveli", "version": 1, "patient": 1}}, "_hard_lock": false, "version": 1, "familyhistory": {"pk": 1, "model": "ftb.familyhistory", "fields": {"consanguinity": false, "patient": 1, "version": 1, "has_family_history": true, "affected_relation": "Uncle"}}, "_locked_by": null, "_locked_at": null, "name": "DeepanS"}}'
        
        self.assertEquals(expected_json_string, Patient.objects.select_related('address', 'details', 'family_history').get(id=patient.id).json_encode())

        
