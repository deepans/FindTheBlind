from django.test import TestCase
from ftb.models import FamilyHistory

class FamilyHistoryTest(TestCase):
    def test_should_validate_family_history_of_the_patient(self):
        FamilyHistory.create(False, )
