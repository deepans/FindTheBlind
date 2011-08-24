import os, sys
sys.path.append('/home/dotcloud/current/server/')
sys.path.append('/home/dotcloud/current/server/json/')
sys.path.append('/home/dotcloud/current/server/ftb/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
import django.core.handlers.wsgi
djangoapplication = django.core.handlers.wsgi.WSGIHandler()
def application(environ, start_response):
    if 'SCRIPT_NAME' in environ:
        del environ['SCRIPT_NAME']
    return djangoapplication(environ, start_response)

