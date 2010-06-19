# Django Settings for Mentortogether project
import os

# ---------------------------------------------------------------------
# Get base settings from the environment.
MT_SITE_ROOT = os.environ['MT_SITE_ROOT']
MT_PROJECT_ROOT = os.environ['MT_PROJECT_ROOT']

# ---------------------------------------------------------------------
# Debug Settings (Enabled by default)
DEBUG = True
TEMPLATE_DEBUG = True

# ---------------------------------------------------------------------
# Email Settings
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USER_TLS = ''

# ---------------------------------------------------------------------
# Filesystem Storage Settings
FS_STOR_ROOT = os.path.join(MT_SITE_ROOT, 'fs_stor')
if not os.path.exists(FS_STOR_ROOT):
    raise Exception('FS_STOR_ROOT (Filesystem storage) not found.')
if not os.path.isdir(FS_STOR_ROOT):
    raise Exception('FS_STOR_ROOT is not a directory.')

# ---------------------------------------------------------------------
# Project Administrators
ADMINS = (
    ('Vivek Thampi', 'vivek@mentortogether.org'),
)
MANAGERS = ADMINS

# ---------------------------------------------------------------------
# We run the server on IST.
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
MEDIA_ROOT = os.path.join(MT_PROJECT_ROOT, 'media')

# ---------------------------------------------------------------------
# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/static'

# ---------------------------------------------------------------------
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

# ---------------------------------------------------------------------
# Database Settings
DATABASE_ENGINE = 'sqlite3'
DATABASE_HOST = ''
DATABASE_NAME = os.path.join(FS_STOR_ROOT, 'database', 'mentortogether.db')
DATABASE_PASSWORD = ''
DATABASE_OPTIONS = ''
DATABASE_PORT = ''
DATABASE_USER = ''

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
TEMPLATE_DIRS = ( os.path.join(MT_PROJECT_ROOT, 'templates'), )

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
PHOTOS_LOCATION = os.path.join(FS_STOR_ROOT, 'photos')
THUMBNAILS_LOCATION = os.path.join(FS_STOR_ROOT, 'thumbnails')

USER_PHOTO_MAX_UPLOAD_SIZE = 512000
USER_PHOTO_MAX_UPLOAD_WIDTH = 800
USER_PHOTO_MAX_UPLOAD_HEIGHT = 1024

USER_PHOTO_DEFAULT_MALE_MENTOR = os.path.join(MEDIA_ROOT, 'imgs', 'male_user_icon.png')
USER_PHOTO_DEFAULT_FEMALE_MENTOR = os.path.join(MEDIA_ROOT, 'imgs', 'female_user_icon.png')
USER_PHOTO_DEFAULT_MALE_MENTEE = os.path.join(MEDIA_ROOT, 'imgs', 'boy_user_icon.png')
USER_PHOTO_DEFAULT_FEMALE_MENTEE = os.path.join(MEDIA_ROOT, 'imgs', 'girl_user_icon.png')

USER_PHOTO_TN_PROFILE_SIZE = [ 150, 200 ]
USER_PHOTO_TN_TAG_SIZE     = [ 80, 80 ]
