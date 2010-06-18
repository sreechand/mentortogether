# django.wsgi - WSGI Interface for Mentortogether Project.
#
#
import os
import sys
import django.core.handlers.wsgi

# MT_SITE_ROOT must be defined by Apache (or the server) that
# invokes this interface. It must point to the application site
# root (see README.)
if 'MT_SITE_ROOT' not in os.environ:
    raise Exception('MT_SITE_ROOT must be defined in the Env')
MT_SITE_ROOT = os.environ['MT_SITE_ROOT']

# MT_PROJECT_ROOT points to the django project that implements the
# mentortogether application. As a convention the project resides in
# the site root under $MT_SITE_ROOT/mentortogether. We also export 
# this as an environment variable for use in the project settings.
MT_PROJECT_ROOT = os.path.join(MT_SITE_ROOT, 'mentortogether')

# Add project root to system path so python module system finds it.
sys.path.append(MT_PROJECT_ROOT)

# Export variables to the application
os.environ['MT_PROJECT_ROOT'] = MT_PROJECT_ROOT
os.environ['DJANGO_SETTINGS_MODULE'] = 'mentortogether.settings'

# Create application.
application = django.core.handlers.wsgi.WSGIHandler()
