from django.test import TestCase
from json.model_factory import ParentFactory, OneToOneParentFactory
from json.tests.models import Parent, OneToOneChild, OneToManyChild, SimpleModelOne, SimpleModelTwo, OneToOneParent
from json.persister import DbObjectLocator, ReplaceLatestMergeStrategy
from json.tests.test_models_manager import TestModelsManager
from json.persister import persist
import simplejson

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
        
    def test_should_convert_multi_level_hierarchical_model_to_its_json_representation(self):
        parent = ParentFactory.create_related()
        expected_json_string = '{"onetoonechild": {"o2o_field1": "o2ofield1value", ' +\
                                                   '"pk": 1, ' +\
                                                   '"model": "tests.onetoonechild", ' +\
                                                   '"o2o_field4": 1, ' +\
                                                   '"o2o_field3": "k2", ' +\
                                                   '"o2o_field2": 100, ' +\
                                                   '"onetomanychild": {"pk": 1, ' +\
                                                                       '"model": "tests.onetomanychild", ' +\
                                                                       '"o2m_field1": "o2mfield1value", ' +\
                                                                       '"o2m_field2": 1}}, ' +\
                                 '"pk": 1, ' +\
                                 '"model": "tests.parent", ' +\
                                 '"p_field1": "pfield1value"}'

        self.assertEquals(simplejson.loads(expected_json_string),
                          simplejson.loads(Parent.objects.select_related('one_to_one_relation').get(id=parent.id).json_encode()))
        
    def test_should_create_new_hierarchical_entities_to_the_database_from_json_string(self):
        self.assertEquals(0, Parent.objects.count())
        self.assertEquals(0, OneToOneChild.objects.count())
        self.assertEquals(0, OneToManyChild.objects.count())

        json_string = '{"onetoonechild": {"o2o_field1": "o2ofield1value", ' +\
                                          '"pk": 1, ' +\
                                          '"model": "tests.onetoonechild", ' +\
                                          '"o2o_field4": 1, ' +\
                                          '"o2o_field3": "k2", ' +\
                                          '"o2o_field2": 100, ' +\
                                          '"onetomanychild": {"pk": 1, ' +\
                                                              '"model": "tests.onetomanychild", ' +\
                                                              '"o2m_field1": "o2mfield1value", ' +\
                                                              '"o2m_field2": 1}}, ' +\
                        '"pk": 1, ' +\
                        '"model": "tests.parent", ' +\
                        '"p_field1": "pfield1value"}'
        
        persist(json_string)
        
        self.assertEquals(1, Parent.objects.count())
        self.assertEquals(1, OneToOneChild.objects.count())
        self.assertEquals(1, OneToManyChild.objects.count())
    
    def tearDown(self):
        self.test_models_manager.revert()

class PersisterTestCase(TestCase):
    def test_should_identify_db_object_by_surragate_key(self):
        parent = ParentFactory.create_related()
        self.assertEquals(parent, DbObjectLocator.identify_by_surragate_key('tests.parent', parent.id))
        
    def test_should_identify_multiple_db_objects_by_surragate_keys(self):
        parent1 = ParentFactory.create_related()
        parent2 = ParentFactory.create_related()

        expected_objects = {parent1.id: parent1,
                            parent2.id: parent2}

        self.assertEquals(expected_objects, DbObjectLocator.identify_all_by_surragate_keys('tests.parent', (parent1.id, parent2.id)))
        
    def test_should_create_or_update_a_simple_db_object_without_any_hierarchy(self):

        self.assertEquals(0, SimpleModelOne.objects.count())
        
        properties = {"field1": "field value",
                      "pk": 1,
                      "model": "tests.simplemodelone",
                      "field2": 1}

        ReplaceLatestMergeStrategy().persist(properties)

        self.assertEquals(1, SimpleModelOne.objects.count())
        object_from_db = SimpleModelOne.objects.get()
        
        self.assertIsNotNone(object_from_db)
        self.assertEquals('field value', object_from_db.field1)
        self.assertEquals(1, object_from_db.field2)

        properties = {"field1": "some new value",
                      "pk": object_from_db.id,
                      "model": "tests.simplemodelone",
                      "field2": 100}

        ReplaceLatestMergeStrategy().persist(properties)

        self.assertEquals(1, SimpleModelOne.objects.count())
        object_from_db = SimpleModelOne.objects.get()
        
        self.assertIsNotNone(object_from_db)
        self.assertEquals('some new value', object_from_db.field1)
        self.assertEquals(100, object_from_db.field2)

    def test_should_create_or_update_a_model_with_one_to_one_child_relation(self):
        self.assertEquals(0, SimpleModelOne.objects.count())
        self.assertEquals(0, SimpleModelTwo.objects.count())
        self.assertEquals(0, OneToOneParent.objects.count())
        
        properties = {"o2o_child1": {"pk": 1,
                                    "model": "tests.simplemodelone",
                                    "field2": 100,
                                    "field1": "Field one"},
                      "o2o_child2": {"pk": 1,
                                     "model": "tests.simplemodeltwo",
                                     "field2": 150,
                                     "field1": "Field one value"},
                      "pk": 1,
                      "model": "tests.onetooneparent",
                      "p_field1": "parent field 1 value"}

        ReplaceLatestMergeStrategy().persist(properties)
        
        self.assertEquals(1, SimpleModelOne.objects.count())
        self.assertEquals(1, SimpleModelTwo.objects.count())        
        self.assertEquals(1, OneToOneParent.objects.count())

        
        
