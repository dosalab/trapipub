from .base import * 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1b6v^%roth(suznu^pe=w!qn119uv)8h!lg)7&4$*=61(dh+r#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
USE_X_FORWARDED_HOST = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tracker-test',
        'USER': 'abu',
        'PASSWORD': 'trackerpwd',
    }
}

