from django.conf.urls.defaults import *
import mentortogether
from mentortogether.user import views

# Enable Admin Interface
from django.contrib import admin
admin.autodiscover()

# Url Controller
urlpatterns = patterns('',
    (r'^$', 'mentortogether.views.homepage'),

    # mentortogether user views
    (r'^u/', include('mentortogether.user.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^dashboard/$', 'mentortogether.views.dashboard'), 
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': 'media'}),
    (r'^imgs/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': 'media/imgs'}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': 'media/css'}),
)
