from django.conf.urls.defaults import *
import mentortogether
import settings
import django.views.static
from mentortogether.user import views

# Enable Admin Interface
from django.contrib import admin
admin.autodiscover()

# Url Controller
urlpatterns = patterns('',
    (r'^$', 'mentortogether.views.homepage'),

    (r'^h/$', 'mentortogether.views.home'),

    # mentortogether user views
    (r'^u/', include('mentortogether.user.urls')),

    # mentortogether user views
    (r'^m/(?P<username>.*)/wp/$', 'mentortogether.mentor.views.wp'),

    (r'^m/(?P<username>.*)/archive/$',
        'mentortogether.mentor.views.archive_index'),

    (r'^m/(?P<username>.*)/archive/(?P<yyyy>[0-9]+)/(?P<mm>[0-9]+)/(?P<dd>[0-9]+)$', 
        'mentortogether.mentor.views.archive'),
    
    (r'^m/(?P<username>.*)/$', 'mentortogether.mentor.views.mentorship'),

    (r'^admin/', include(admin.site.urls)),

    (r'^dashboard/$', 'mentortogether.views.dashboard'), 

    # Map MEDIA_URL to MEDIA_ROOT
    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
        django.views.static.serve, { 'document_root' : settings.MEDIA_ROOT } ),
    (r'^imgs/(?P<path>.*)$',
        django.views.static.serve, { 'document_root' : 'media/imgs' } ),
    (r'^css/(?P<path>.*)$',
        django.views.static.serve, { 'document_root' : 'media/css' } )
)
