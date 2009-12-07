from django.conf.urls.defaults import *
import views
import settings

urlpatterns = patterns('',
    (r'^$', 'mentortogether.user.views.upage' ),
    
    (r'^apply/(?P<role>.*)/$', 'mentortogether.user.views.apply'),

    (r'^activate/(?P<key>.*)$', 'mentortogether.user.views.activate'),

    (r'^login/$', 'django.contrib.auth.views.login', 
        { 'template_name' : 'user/login.html' }),

    (r'^logout/$', 'django.contrib.auth.views.logout', 
        { 'template_name' : 'user/logged_out.html' }),

    (r'^password/change/$', 'django.contrib.auth.views.password_change',
        { 'template_name' : 'user/password_change_form.html' }),

    (r'^password/change/done/$', 'django.contrib.auth.views.password_change_done',
        { 'template_name' : 'user/password_change_done.html' }),

    (r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        { 'template_name' : 'user/password_reset_form.html' }),

    (r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done',
        { 'template_name' : 'user/password_reset_done.html' }),

    (r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete',
        { 'template_name' : 'user/password_reset_complete.html' }),

    (r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm',
        { 'template_name' : 'user/password_reset_confirm.html' }),
    
    # user photo views
    (r'^(?P<username>.*)/photo/$', views.photo),
    (r'^(?P<username>.*)/photo/image/(?P<type>.*)/$', views.photo_image),
    (r'^(?P<username>.*)/photo/upload/$', views.photo_upload),

    # profile views
    (r'^(?P<username>.*)/profile/$', 'mentortogether.user.views.profile_view'),
    (r'^(?P<username>.*)/profile/edit/$', 'mentortogether.user.views.profile_edit'),

)
