import settings
from fabric.api import local, hide

def setup_db():
    with hide('stdout'):
        local("export PGPASSWORD='{0}'".format(settings.DATABASES['default']['PASSWORD']))
        local('sudo -u postgres psql postgres -c "drop database if exists {0};"'.format(settings.DATABASES['default']['NAME']))
        local('sudo -u postgres psql postgres -c "drop user if exists {0};"'.format(settings.DATABASES['default']['USER']))
        local('sudo -u postgres psql postgres -c "create user {0} with password \'{1}\' CREATEDB;"'.format(settings.DATABASES['default']['USER'], settings.DATABASES['default']['PASSWORD']))
        local('sudo -u postgres psql postgres -c "create database {0};"'.format(settings.DATABASES['default']['NAME']))
        local('sudo -u postgres psql postgres -c "grant all privileges on database {0} to {1};"'.format(settings.DATABASES['default']['NAME'], settings.DATABASES['default']['USER']))
def sync_db():
    local('python manage.py syncdb --noinput')

def db():
    setup_db()
    sync_db()
    setup_admin()

def test():
    local('python manage.py test')
    
def setup_admin():
    local('python manage.py createsuperuser --username=admin --email=admin@ftb.com')

    
    
