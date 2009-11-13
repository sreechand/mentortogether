from settings_base import *

MT_ROOT_PATH        = '/home/vivek/mentortogether.org/'

DEBUG               = False
TEMPLATE_DEBUG      = DEBUG

DATABASE_ENGINE     = 'sqlite3'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME       = MT_ROOT_PATH + 'database/db.prod' # Or path to database file if using sqlite3.
DATABASE_USER       = ''         # Not used with sqlite3.
DATABASE_PASSWORD   = ''         # Not used with sqlite3.
DATABASE_HOST       = ''         # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT       = ''         # Set to empty string for default. Not used with sqlite3.

TEMPLATE_DIRS = (
    MT_ROOT_PATH + 'public/mentortogether/templates' 
)

EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = 'admin@mentortogether.org'
EMAIL_HOST_PASSWORD = 'mtStaff65'
EMAIL_USE_TLS       = True
