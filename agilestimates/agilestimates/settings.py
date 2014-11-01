# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
     ('superuser', 'marcelo.cure@ilegra.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'postgres',                   # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'postgres',
        'PASSWORD': 't00thbrush',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

ALLOWED_HOSTS = ['*']

STATIC_ROOT = 'C:/Users/Marcelo Cure/Documents/github/agile-estimates/agilestimates/aep/all_static/'

TEMPLATE_DIRS = (

    'C:/Users/Marcelo Cure/Documents/github/agile-estimates/agilestimates/aep/templates',
    'C:/Users/Marcelo Cure/Documents/github/agile-estimates/agilestimates/agilestimates/template',
)

STATIC_URL = '/static/'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '80-yvv(ybl%*a87dt2u&1wd03lq61tm_1wfn(k5_dechsjzk+d'

STATICFILES_DIRS = (

    'C:/Users/Marcelo Cure/Documents/github/agile-estimates/agilestimates/all_static',

)





# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'aep',
    'django_coverage',
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=foo,bar',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'agilestimates.urls'

WSGI_APPLICATION = 'agilestimates.wsgi.application'

SUIT_CONFIG = {
    'ADMIN_NAME': 'Agile Estimates Support',
}

ROOT_URLCONF = 'agilestimates.urls'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


trello_api_key = '500883312ee38a44d357b1ac15a17524'
trello_auth_token = '5e6a4b22d58ffd3e79c59ceba2f72cc3023be1397284b005ee57090be0a5e1e3'

import sys

if 'test' in sys.argv:
    try:
        from test import *
    except ImportError:
        pass