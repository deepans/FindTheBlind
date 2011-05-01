from django.test import TestCase
from ftb.models import Patient

class PatientTest(TestCase):
    def test_should_create_a_patient(self):
        count = Patient.objects.count()
        raju = Patient.save_or_update(name='raju', fathers_name='mohan')
        self.assertEqual(count + 1, Patient.objects.count())
        self.assertEqual('raju', raju.name)
        self.assertEqual('mohan', raju.fathers_name)
