from django.db.models.signals import pre_save

def validate_model(sender, **kwargs):
    if 'raw' in kwargs and not kwargs['raw'] and kwargs['instance'].__module__ == 'ftb.models':
        kwargs['instance'].full_clean()

pre_save.connect(validate_model, dispatch_uid='validate_models')
