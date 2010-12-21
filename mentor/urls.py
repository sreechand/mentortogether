#
# copyright (c) 2010 Mentortogether
#
from django.conf.urls.defaults import patterns, url
from mentortogether.mentor import views

urlpatterns = patterns('',
    url(r'^(?P<mid>\d+)/$', 
        views.mentorship, name="mentorship"),
    url(r'^(?P<mid>\d+)/prompt/$', 
        views.prompt_listing, name="prompt-listing"),
    url(r'^(?P<mid>\d+)/prompt/(?P<pid>\d+)/start$', 
        views.prompt_start, name="prompt-start"),
    url(r'^(?P<mid>\d+)/prompt/(?P<pid>\d+)/stop$', 
        views.prompt_stop, name="prompt-stop"),
    url(r'^(?P<mid>\d+)/msg/$', 
        views.thread_listing, name="thread-listing"),
    url(r'^(?P<mid>\d+)/msg/new/$', 
        views.new_thread, name="new-thread"),
    url(r'^(?P<mid>\d+)/msg/(?P<tid>\d+)/post/$', 
        views.post_message, name="post-message"),
    url(r'^(?P<mid>\d+)/msg/(?P<tid>\d+)/$', 
        views.view_thread, name="view-thread"),
)
