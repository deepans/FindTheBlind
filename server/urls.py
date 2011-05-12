from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    (r'^ftb/', include('ftb.urls')),                       
    (r'^admin/', include('locking.urls')),
#    (r'', include('staticfiles.urls')),                       
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^server/', include('server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
