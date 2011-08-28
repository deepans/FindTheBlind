from django.forms.models import ModelForm
from ftb.models import FamilyHistory
from settings import STATIC_URL

class EnhancedModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnhancedModelForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'field_dependency'):
            for field_name, dependent_fields in self.field_dependency.iteritems():
                for dependent_field_name, dependent_value in dependent_fields:
                    widget_attrs = self.fields[dependent_field_name].widget.attrs
                    existing_class = widget_attrs.get('class') if widget_attrs.get('class') else ''
                    widget_attrs.update({'class' : '{0} depends_on-{1}-with_value-{2}'.format(existing_class,
                                                                                             field_name,
                                                                                             dependent_value)})
class FamilyHistoryForm(EnhancedModelForm):
    field_dependency = {'has_family_history': (('affected_relation', 'Yes'), ('consanguinity', 'Yes'))}
    
    class Meta:
        model = FamilyHistory

class TabbedForm(ModelForm):

    class Media:
        css = {'all': ('{0}tabbedadmin/css/tabs.css'.format(STATIC_URL),) }
