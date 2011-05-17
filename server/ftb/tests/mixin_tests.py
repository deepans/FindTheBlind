from django.test import TestCase
from ftb.models import Patient
from ftb.exceptions import StaleObjectException

class ConcurrentlyModifiableTest(TestCase):
    def test_should_update_model_concurrently_with_optimistic_locking(self):
        patient = Patient.objects.create(name='Deepan')
        patient_read_again = Patient.objects.get(name='Deepan')

        patient.name = 'Deepan Subramani'
        patient_read_again.name = 'Deepan S'

        Patient.concurrency.update(patient)
        self.assertEquals(2, Patient.objects.get(name='Deepan Subramani').version)
        self.assertRaises(Patient.DoesNotExist, Patient.objects.get, name='Deepan')
        self.assertRaises(StaleObjectException, Patient.concurrency.update, patient_read_again)