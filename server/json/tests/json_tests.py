from django.test import TestCase
from json.tests.test_models_manager import TestModelsManager

class JsonTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestModelsManager, self).__init__(*args, **kwargs)
        self.test_models_manager = TestModelsManager()
    
        
    def tearDown(self):
        self.test_models_manager.revert()
