from django.test import TestCase
from json.model_factory import ParentFactory
from json.tests.models import Parent, OneToOneChild, OneToManyChild, SimpleModelOne, SimpleModelTwo,\
     OneToOneParent, ReverseOneToOneChild, OneToManyParent, ReverseOneToManyChild, SimpleModelThree,\
     SimpleModelFour
from json.persister import DbObjectLocator, ReplaceLatestMergeStrategy
from json.tests.test_models_manager import TestModelsManager
import simplejson

def setUp(self):
    self.test_models_manager = TestModelsManager()
    self.test_models_manager.set(INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'json',
        'json.tests',
        'django_nose',))

def tearDown(self):
    self.test_models_manager.revert()

'''
class JsonTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(JsonTestCase, self).__init__(*args, **kwargs)


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
                          simplejson.loads(Parent.objects.get(id=parent.id).json_encode()))
        
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
        
        ReplaceLatestMergeStrategy().persist(json_string)
        
        self.assertEquals(1, Parent.objects.count())
        self.assertEquals(1, OneToOneChild.objects.count())
        self.assertEquals(1, OneToManyChild.objects.count())
'''    
class PersisterTestCase(TestCase):
    
    def test_should_identify_db_object_by_surragate_key(self):
        parent = ParentFactory.create_related()
        self.assertEquals(parent, DbObjectLocator.identify_by_surragate_key('tests.parent', parent.id))
        self.assertEquals(None, DbObjectLocator.identify_by_surragate_key('tests.parent', None))
        
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

    def test_should_create_or_update_a_model_with_one_to_many_children_relation(self):
        # create scenario
        self.assertEquals(0, SimpleModelThree.objects.count())
        self.assertEquals(0, SimpleModelFour.objects.count())
        self.assertEquals(0, OneToManyParent.objects.count())
        self.assertEquals(0, ReverseOneToManyChild.objects.count())

        properties = { "model" : "tests.onetomanyparent",
                       "o2m_child1" : { "field1" : "Field one",
                                        "field2" : 100,
                                        "model" : "tests.simplemodelthree",
                                        "onetomanyparent_rel" : [ 1 ],
                                        "pk" : 1},
                       "o2m_child2" : { "field1" : "Field one value",
                                        "field2" : 150,
                                        "model" : "tests.simplemodelfour",
                                        "onetomanyparent_set" : [ 1 ],
                                        "pk" : 1},
                       "p_field1" : "parent field 1 value",
                       "pk" : 1,
                       "reverseonetomanychild" : [ { "field1" : "Field 1 value",
                                                     "field2" : 199,
                                                     "field3" : 1,
                                                     "model" : "tests.reverseonetomanychild",
                                                     "pk" : 1},
                                                   { "field1" : "some test",
                                                     "field2" : 100,
                                                     "field3" : 1,
                                                     "model" : "tests.reverseonetomanychild"}
                                               ]
                   }
        
        ReplaceLatestMergeStrategy().persist(properties)
        self.assertEquals(1, SimpleModelThree.objects.count())
        self.assertEquals(1, SimpleModelFour.objects.count())
        self.assertEquals(1, OneToManyParent.objects.count())
        self.assertEquals(2, ReverseOneToManyChild.objects.count())
        
        
    def test_should_create_or_update_a_model_with_one_to_one_child_relation(self):
        # create scenario
        self.assertEquals(0, SimpleModelOne.objects.count())
        self.assertEquals(0, SimpleModelTwo.objects.count())
        self.assertEquals(0, OneToOneParent.objects.count())
        self.assertEquals(0, ReverseOneToOneChild.objects.count())
        
        properties = {"o2o_child1": {"model": "tests.simplemodelone",
                                    "field2": 100,
                                    "field1": "Field one"},
                      "o2o_child2": {"pk": 1,
                                     "model": "tests.simplemodeltwo",
                                     "field2": 150,
                                     "field1": "Field one value"},
                      "reverseonetoonechild": {"pk": 1,
                                               "model": "tests.reverseonetoonechild",
                                               "field2": 199,
                                               "field1": "Field 1 value",
                                               "field3": 1},
                      "pk": 1,
                      "model": "tests.onetooneparent",
                      "p_field1": "parent field 1 value"}

        ReplaceLatestMergeStrategy().persist(properties)
        
        self.assertEquals(1, SimpleModelOne.objects.count())
        self.assertEquals(1, SimpleModelTwo.objects.count())
        self.assertEquals(1, ReverseOneToOneChild.objects.count())
        self.assertEquals(1, OneToOneParent.objects.count())

        expected_json = '{"o2o_child1": {"pk": 1,' +\
                                        '"model": "tests.simplemodelone",' +\
                                        '"field2": 100,' +\
                                        '"field1": "Field one",' +\
                                        '"onetooneparent": 1},' +\
                         '"o2o_child2": {"pk": 1,' +\
                                        '"model": "tests.simplemodeltwo",' +\
                                        '"field2": 150,' +\
                                        '"field1": "Field one value",' +\
                                        '"onetooneparent": 1},' +\
                         '"reverseonetoonechild": {"pk": 1,' +\
                                                 '"model": "tests.reverseonetoonechild",' +\
                                                 '"field2": 199,' +\
                                                 '"field1": "Field 1 value",' +\
                                                 '"field3": 1},' +\
                         '"pk": 1,' +\
                         '"model": "tests.onetooneparent",' +\
                         '"p_field1": "parent field 1 value"}'

        self.assertEquals(simplejson.loads(expected_json),
                          simplejson.loads(OneToOneParent.objects.get(p_field1='parent field 1 value').json_encode()))

        # update scenario 
        updated_properties = {"o2o_child1": {"pk": 1,
                                             "model": "tests.simplemodelone",
                                             "field2": 199,
                                             "field1": "Field one updated"},
                              "o2o_child2": {"pk": 1,
                                             "model": "tests.simplemodeltwo",
                                             "field2": 250,
                                             "field1": "Field one value updated"},
                              "reverseonetoonechild": {"pk": 1,
                                                       "model": "tests.reverseonetoonechild",
                                                       "field2": 399,
                                                       "field1": "Field 1 value updated",
                                                       "field3": 1},

                              "pk": 1,
                              "model": "tests.onetooneparent",
                              "p_field1": "parent field 1 value updated"}
        
        ReplaceLatestMergeStrategy().persist(updated_properties)

        expected_updated_json = '{"o2o_child1": {"pk": 1,' +\
                                                '"model": "tests.simplemodelone",' +\
                                                '"field2": 199,' +\
                                                '"field1": "Field one updated",' +\
                                                '"onetooneparent": 1},' +\
                                 '"o2o_child2": {"pk": 1,' +\
                                                '"model": "tests.simplemodeltwo",' +\
                                                '"field2": 250,' +\
                                                '"field1": "Field one value updated",' +\
                                                '"onetooneparent": 1},' +\
                                '"reverseonetoonechild": {"pk": 1,' +\
                                                         '"model": "tests.reverseonetoonechild",' +\
                                                         '"field2": 399,' +\
                                                         '"field1": "Field 1 value updated",' +\
                                                         '"field3": 1},' +\
                                 '"pk": 1,' +\
                                 '"model": "tests.onetooneparent",' +\
                                 '"p_field1": "parent field 1 value updated"}'

        self.assertRaises(OneToOneParent.DoesNotExist, OneToOneParent.objects.get, p_field1='parent field 1 value')
        
        self.assertEquals(simplejson.loads(expected_updated_json),
                          simplejson.loads(OneToOneParent.objects.get(p_field1='parent field 1 value updated').json_encode()))
        

        