from django.conf.urls.defaults import *
import mentortogether

# Enable Admin Interface
from django.contrib import admin
admin.autodiscover()

# Url Controller
urlpatterns = patterns('',
    (r'^admin/',   include(admin.site.urls)),
    (r'^signup/$', 'mentortogether.mt_user.views.signup')
)
