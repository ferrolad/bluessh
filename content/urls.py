#coding=utf-8

from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('content.views',
                       url(r'^get_menu/$', get_menu),
                       url(r'^get_notice/$', get_notice),
                       #url(r'^status/$',show_vps_status),
                       url(r'^freessh/$', show_freessh),
                       url(r'^post_freessh/$', post_freessh),
                       url(r'^(.*)/$', show_content),  # 确保在最后
                       )
