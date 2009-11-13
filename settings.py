import os
import sys

if os.getenv( "DJANGO_SETTINGS" )   == "production":
    from admin.settings_production import *
elif os.getenv( "DJANGO_SETTINGS" ) == "beta":
    from admin.settings_beta import *
else:
    from admin.settings_debug import *
