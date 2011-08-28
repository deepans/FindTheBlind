from django.db.models.loading import get_model
from django.db.models.fields.related import OneToOneField, ForeignKey
from collections import Iterable
import simplejson

def persist(json_string, strategy):
    json = simplejson.loads(json_string)
    if isinstance(json, Iterable):
        return [strategy().persist(item) for item in json]
    else:
        return strategy().persist(json)

class ReplaceLatestMergeStrategy(object):
    def _handle_field(self, db_object, field, value):
        setattr(db_object, field.name, value)
        return db_object

    def _handle_forward_rel(self, db_object, field, properties):
        setattr(db_object, field.name, self.persist(properties))
        return db_object

    def _handle_relation(self, db_object, field, properties):
        return {OneToOneField: self._handle_forward_rel,
                ForeignKey: self._handle_forward_rel}[type(field)](db_object, field, properties)

    def _handle_reverse_rel(self, relation, parent, properties):
        self.persist(properties, parent=parent)
            
    def _handle_reverse_one_to_many_rel(self, relation, parent, properties):
        if properties:
            model_cls = DbObjectLocator.get_class_from_name(properties[0]['model'])
            parent_field = reduce(lambda acc, field: field if field.rel and parent and type(parent) is field.rel.to else acc,
                                  model_cls._meta.fields, None)

            model_cls.objects.filter(**{parent_field.name:parent}).delete()

            for item_properties in properties:
                self._handle_reverse_rel(relation, parent, item_properties)
        
    def merge_and_persist(self, model_cls, db_object, properties, parent=None):
        for field in model_cls._meta.fields:
            if properties.has_key(field.name):
                if not field.rel:
                    db_object = self._handle_field(db_object, field, properties[field.name])
                else:
                    if parent and type(parent) is field.rel.to:
                        setattr(db_object, field.name, parent)
                    else:
                        db_object = self._handle_relation(db_object, field, properties[field.name])

        db_object.save()

        
        for relation in model_cls._meta.get_all_related_objects():
            if properties.has_key(relation.var_name):
                {OneToOneField: self._handle_reverse_rel,
                 ForeignKey: self._handle_reverse_one_to_many_rel}[type(relation.field)](relation, db_object, properties[relation.var_name])
            

        return db_object

    def persist(self, properties, parent=None):
        if not properties:
            return None

        model_name = properties.pop('model')
        model_cls = DbObjectLocator.get_class_from_name(model_name)
        db_object = DbObjectLocator.identify_by_surragate_key(model_name, properties.pop('pk')) if properties.has_key('pk') else None

        db_object = db_object if db_object else model_cls()
        
        return self.merge_and_persist(model_cls, db_object, properties, parent)

class DbObjectLocator(object):

    @classmethod
    def get_class_from_name(cls, model_name):
        app_name, model_name = model_name.split('.')
        return get_model(app_name, model_name)
    
    @classmethod
    def identify_by_surragate_key(cls, model_name, value):
        if value:
            model_class = cls.get_class_from_name(model_name)

            try:
                return model_class.objects.get(**{model_class._meta.pk.name:value})
            except model_class.DoesNotExist:
                return None
        return None

    @classmethod
    def identify_all_by_surragate_keys(cls, model_name, values):
        model_class = cls.get_class_from_name(model_name)
        return dict([(object.id, object) for object in model_class.objects.filter(**{model_class._meta.pk.name + '__in': values})])

