from django.conf.urls.defaults import *
import mentortogether
import settings
import django.views.static
from mentortogether.user import views

# Enable Admin Interface
from django.contrib import admin
admin.autodiscover()

# FIXME: Split urls into apps

# Url Controller
urlpatterns = patterns('',

    url(r'^$', 
        view='mentortogether.views.root', name='welcome'),

    url(r'^h/$', 
        view='mentortogether.views.home', name='user-home'),

    (r'^admin/',    include(admin.site.urls)),
    (r'^u/',        include('mentortogether.user.urls')),
    (r'^m/',        include('mentor.urls')), 

    # mentortogether user views
    # (r'^m/(?P<username>.*)/wp/$', 'mentortogether.mentor.views.wp'),

    # (r'^m/(?P<username>.*)/archive/$',
    #     'mentortogether.mentor.views.archive_index'),

    # (r'^m/(?P<username>.*)/archive/(?P<yyyy>[0-9]+)/(?P<mm>[0-9]+)/(?P<dd>[0-9]+)$', 
    #     'mentortogether.mentor.views.archive'),
    # 
    # (r'^m/(?P<username>.*)/$', 'mentortogether.mentor.views.mentorship'),


   
    # Curriculum views
    # (r'^a/curriculum/', include('curriculum.urls')), 

    (r'^_debug/$', 'mentortogether.views.debug' ),

    # Map MEDIA_URL to MEDIA_ROOT
    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
        django.views.static.serve, { 'document_root' : settings.MEDIA_ROOT } ),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': 'media'}),
    (r'^imgs/(?P<path>.*)$',
        django.views.static.serve, { 'document_root' : 'media/imgs' } ),
    (r'^css/(?P<path>.*)$',
        django.views.static.serve, { 'document_root' : 'media/css' } )
)
