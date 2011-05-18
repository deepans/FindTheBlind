from django.test import TestCase
from ftb.models import FamilyHistory
from django.core.exceptions import ValidationError

class FamilyHistoryTest(TestCase):
    def test_should_validate_family_history(self):
        self.assertRaisesRegexp(ValidationError,
                                "Should'nt has_family_history is true?",
                                FamilyHistory.objects.create,
                                has_family_history=False,
                                affected_relation='Uncle',
                                consanguinity=False)