from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('test.views',
                       url(r'^test/$', test),
                       url(r'^mail_test/$', mail_test),
                       #url(r'^create_ssh/$',create_ssh_test),
                       #url(r'^delete_ssh/$',delete_ssh_test),

                       )
