from django.test import TestCase
from json.model_factory import ParentFactory
from json.tests.models import Parent
from json.tests.test_models_manager import TestModelsManager

class JsonTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(JsonTestCase, self).__init__(*args, **kwargs)
        self.test_models_manager = TestModelsManager()
        self.test_models_manager.set(INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'json',
                'json.tests',
                'django_nose',))
                
    def test_should_encode_a_model_into_json_representation(self):
        parent = ParentFactory.create_related()
        expected_json_string = '{}'
        self.assertEquals(expected_json_string, Parent.objects.select_related('one_to_one_relation').get(id=parent.id).json_encode())
        
    def tearDown(self):
        self.test_models_manager.revert()
