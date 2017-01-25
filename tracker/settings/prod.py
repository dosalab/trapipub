from .base import * 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9x_*ed6&v=gnaask$y6r@!z4af%!#*--*z%y-0uki2&uau83uy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#SITE_ID = 1
USE_X_FORWARDED_HOST = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tracker',
        'USER': 'ubuntu',
    }
}

