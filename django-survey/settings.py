from djangoappengine.settings_base import *
import os

# Uncomment this line for deployment mode.
#DEBUG = False 

# Uncomment this line for development mode.
DEBUG = True

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    'djangoappengine',
    'djangotoolbox',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'survey',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

# Uncomment this line for deployment.
#ALLOWED_HOSTS = ['django-survey.appspot.com']

# Uncomment this line for development.
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

LOGIN_REDIRECT_URL = '/survey/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'