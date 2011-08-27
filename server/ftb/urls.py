from django.conf.urls.defaults import patterns

urlpatterns = patterns('ftb',
                       (r'(?i)patients', 'views.patients'),
                       
)
