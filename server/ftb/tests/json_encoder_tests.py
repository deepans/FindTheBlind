from django.test import TestCase
from ftb.models import Patient
from ftb.model_factory import PatientFactory

class JsonEncoderTest(TestCase):
    def test_should_encode_a_model_into_json_representation(self):
        patient = PatientFactory.create_related()
        expected_json_string = '{"patientdetails": {"patient": 1, "visual_loss_age": 99, "age": 29, "sex": "M", "ethnic_group": "Hindu", "version": 1, "pk": 1, "model": "ftb.patientdetails"}, "_locked_by": null, "_hard_lock": false, "version": 1, "familyhistory": {"has_family_history": true, "version": 1, "patient": 1, "affected_relation": "Uncle", "pk": 1, "model": "ftb.familyhistory", "consanguinity": false}, "address": {"town": "Neyveli", "pk": 1, "model": "ftb.address", "version": 1, "patient": 1}, "_locked_at": null, "pk": 1, "model": "ftb.patient", "name": "DeepanS"}'

        self.assertEquals(expected_json_string, Patient.objects.select_related('address', 'details', 'family_history').get(id=patient.id).json_encode())

        
