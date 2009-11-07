from django.conf.urls.defaults import *
import mentortogether

# Enable Admin Interface
from django.contrib import admin
admin.autodiscover()

# Url Controller
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^user/signup/(.*)$', 'mentortogether.mt_user.views.signup'),
    (r'^user/activate/(?P<key>.*)$', 'mentortogether.mt_user.views.activate'),
    (r'^login/$', 'django.contrib.auth.views.login', 
        { 'template_name' : 'login.html' }),
    (r'^logout/$', 'django.contrib.auth.views.logout', 
        { 'template_name' : 'logout.html',
          'next_page'     : '/' }),
    (r'^user/chpass/$', 'django.contrib.auth.views.password_change', 
        { 'template_name' : 'chpass.html',
          'post_change_redirect' : '/user/account' }),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': 'css'})
)
