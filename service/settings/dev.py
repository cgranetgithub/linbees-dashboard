from prod import *

DEBUG = True
TEMPLATE_DEBUG = True
#ALLOWED_HOSTS = []

SECRET_KEY = '(jut!-c_9j^a==v$+6(-w3x7v#%*ljd7y2h0w-=*d4r@f5hy-z'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangodb',
        'USER': 'charles',
        'PASSWORD': 'sc39cf63',
        'HOST': 'localhost',
        'PORT': '',
    }
}

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.remove('storages')
INSTALLED_APPS.append('django_extensions')
INSTALLED_APPS = tuple(INSTALLED_APPS)
del STATICFILES_STORAGE
del DEFAULT_FILE_STORAGE
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
