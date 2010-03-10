# Django Settings for Mentortogether project
import os
from local_settings import *

# ---------------------------------------------------------------------
# We depend on DJANGO_MT_ROOT being set in the environment
# so we can deduce the settings for a running instance of the 
# application. (Default to present working directory.)
PROJECT_ROOT = os.getenv('DJANGO_MT_ROOT', os.getcwd())

# Validate PROJECT_ROOT
if not os.path.exists(PROJECT_ROOT):
    raise Exception('PROJECT_ROOT=%s is not valid.' % PROJECT_ROOT)

# ---------------------------------------------------------------------
# The environment can also enable debugging via the DJANGO_MT_DEBUG 
# set to "enable" (default) or "disable".
if os.getenv('DJANGO_MT_DEBUG', 'enable') == 'disable':
    DEBUG = False
else:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

# ---------------------------------------------------------------------
# Setup Path
PATH_MEDIA = os.path.join(PATH_SRC, 'media')
PATH_TEMPLATES = os.path.join(PATH_SRC, 'templates')

# ---------------------------------------------------------------------
# Project Administrators
ADMINS = (
    ('Vivek Thampi', 'vivek.thampi@velocetechnologies.com'),
)
MANAGERS = ADMINS

# ---------------------------------------------------------------------
# We run the server at Kolkata time zone:
# Choices can be found here: 
#    http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Asia/Kolkata'

# ---------------------------------------------------------------------
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# ---------------------------------------------------------------------
# ID of the website. Leave this alone.
SITE_ID = 1

# ---------------------------------------------------------------------
# We disable internalization, because:
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# ---------------------------------------------------------------------
# External API URLS
EXTAPI_URLS = { 
    'YUI_URL': 'http://ajax.googleapis.com/ajax/libs/yui/2.8.0r4'
}

# ---------------------------------------------------------------------
# Absolute path to the directory that holds media.
MEDIA_ROOT = PATH_MEDIA

# ---------------------------------------------------------------------
# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/static/'

# ---------------------------------------------------------------------
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

# ---------------------------------------------------------------------
# Database Settings
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = PATH_DB

# ---------------------------------------------------------------------
# Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media"
)

# ---------------------------------------------------------------------
# Template locations
TEMPLATE_DIRS = ( PATH_TEMPLATES, )

# ---------------------------------------------------------------------
# Misc. Internal Settings
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

ROOT_URLCONF = 'mentortogether.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'mentortogether.user',
    'mentortogether.mentor',
    'mentortogether.cms'
)

LOGIN_URL = '/u/login'
LOGIN_REDIRECT_URL = '/h/'
AUTH_PROFILE_MODULE = 'user.UserProfile'

# ---------------------------------------------------------------------
# User photo settings
PHOTOS_LOCATION = os.path.join(PATH_STATIC, 'photos')
THUMBNAILS_LOCATION = os.path.join(PATH_STATIC, 'thumbnails')

USER_PHOTO_MAX_UPLOAD_SIZE = 512000
USER_PHOTO_MAX_UPLOAD_WIDTH = 800
USER_PHOTO_MAX_UPLOAD_HEIGHT = 1024

USER_PHOTO_DEFAULT_MALE_MENTOR = os.path.join(PATH_MEDIA, 'imgs', 'male_user_icon.png')
USER_PHOTO_DEFAULT_FEMALE_MENTOR = os.path.join(PATH_MEDIA, 'imgs', 'female_user_icon.png')
USER_PHOTO_DEFAULT_MALE_MENTEE = os.path.join(PATH_MEDIA, 'imgs', 'boy_user_icon.png')
USER_PHOTO_DEFAULT_FEMALE_MENTEE = os.path.join(PATH_MEDIA, 'imgs', 'girl_user_icon.png')

USER_PHOTO_TN_PROFILE_SIZE = [ 150, 200 ]
USER_PHOTO_TN_TAG_SIZE     = [ 80, 80 ]
