from django.db.models.loading import get_model

def persist(json_string):
    pass

class ReplaceLatestMergeStrategy(object):
    def merge_simple_db_object(self, db_object, **properties):
        for name, value in properties.iteritems():
            setattr(db_object, name, value)
        db_object.save()

class SimpleDbObjectPersister(ReplaceLatestMergeStrategy):
    def persist(self, properties):
        model_name = properties.pop('model')
        model_cls = DbObjectLocator.get_class_from_name(model_name)
        db_object = DbObjectLocator.identify_by_surragate_key(model_name, properties.pop('pk'))

        if db_object:
            self.merge_simple_db_object(db_object, **properties)
        else:
            model_cls(**properties).save()

class OneToOneFwdRelPersister(ReplaceLatestMergeStrategy):
    def persist(self, properties):
        pass
            
class DbObjectLocator(object):

    @classmethod
    def get_class_from_name(cls, model_name):
        app_name, model_name = model_name.split('.')
        return get_model(app_name, model_name)
    
    @classmethod
    def identify_by_surragate_key(cls, model_name, value):
        model_class = cls.get_class_from_name(model_name)

        try:
            return model_class.objects.get(**{model_class._meta.pk.name:value})
        except model_class.DoesNotExist:
            return None

    @classmethod
    def identify_all_by_surragate_keys(cls, model_name, values):
        model_class = cls.get_class_from_name(model_name)
        return dict([(object.id, object) for object in model_class.objects.filter(**{model_class._meta.pk.name + '__in': values})])
        
