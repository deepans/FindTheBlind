import settings
from fabric.api import local, hide

def reset_db():
    with hide('stdout', 'stderr'):
        local("export PGPASSWORD='{0}'".format(settings.DATABASES['default']['PASSWORD']))
        local('sudo -u postgres psql postgres -c "drop database if exists {0};"'.format(settings.DATABASES['default']['NAME']))
        local('sudo -u postgres psql postgres -c "create database {0};"'.format(settings.DATABASES['default']['NAME']))
        local('sudo -u postgres psql postgres -c "grant all privileges on database {0} to {1};"'.format(settings.DATABASES['default']['NAME'], settings.DATABASES['default']['USER']))

def sync_db():
    local('python manage.py syncdb --noinput')

def db():
    reset_db()
    sync_db()

def test():
    local('python manage.py test')
    


    
    