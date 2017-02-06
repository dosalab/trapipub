from .base import * 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9x_*ed6&v=gnaask$y6r@!z4af%!#*--*z%y-0uki2&uau83uy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

USE_X_FORWARDED_HOST = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'tracker',
        'USER': 'ubuntu',
    }
}

STATIC_ROOT = '/home/ubuntu/static'

