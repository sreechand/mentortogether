from settings_base import *

MT_ROOT_PATH        = '/home/vivek/mentortogether.org/'

DEBUG               = True
TEMPLATE_DEBUG      = DEBUG

DATABASE_ENGINE     = 'sqlite3'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME       = '/home/vivek/mentortogether.org/database/db.debug'       # Or path to database file if using sqlite3.
DATABASE_USER       = ''         # Not used with sqlite3.
DATABASE_PASSWORD   = ''         # Not used with sqlite3.
DATABASE_HOST       = ''         # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT       = ''         # Set to empty string for default. Not used with sqlite3.

TEMPLATE_DIRS = (
    "/Users/vivek/MentorTogether/mentortogether/templates"
)

EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = 'vivek@mentortogether.org'
EMAIL_HOST_PASSWORD = 'qwpo1209'
EMAIL_USE_TLS       = True
