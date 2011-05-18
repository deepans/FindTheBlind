from django.test import TestCase
from ftb.models import FamilyHistory
from django.core.exceptions import ValidationError

class FamilyHistoryTest(TestCase):
    def test_should_validate_while_creating_and_updating_models(self):
        self.assertRaisesRegexp(ValidationError,
                                "Should'nt has_family_history is true?",
                                FamilyHistory.objects.create,
                                has_family_history=False,
                                affected_relation='Uncle',
                                consanguinity=False)
        
        family_history = FamilyHistory.objects.create(has_family_history=True,
                                                      affected_relation='Uncle',
                                                      consanguinity=True)
        family_history.has_family_history = False
        family_history.affected_relation = None
        
        self.assertRaisesRegexp(ValidationError,
                                "Should'nt has_family_history is true?",
                                FamilyHistory.concurrency.update,
                                family_history)