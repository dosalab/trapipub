import pytest
from django.conf import settings

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'testdb',
        'USER': 'abu',
        'PASSWORD': 'trackerpwd',
        }

@pytest.fixture
def server(xprocess):

    def preparefunc(cwd):
        print (str(cwd))
        n = cwd.new(basename="").new(basename="").dirpath().chdir()
        print ("Working directory is {}".format(n))
        path = cwd.join("../../manage.py").strpath
        print(path)
        return (r".*Quit.*", ["python", path, "runserver", "8000"])
    
    logfile = xprocess.ensure("tracker-server", preparefunc)
