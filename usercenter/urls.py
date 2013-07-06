#coding=utf-8
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import *
from views import *

urlpatterns = patterns('usercenter.views',
        url(r'^$',usercenter_home),
        url(r'^login/$',  login,{'template_name':'usercenter/login.html'}),
        url(r'^logout/$',logout,{'template_name':'usercenter/logout.html'}),
        url(r'^reg/$',register),
        url(r'^confirm/(?P<ver_code>.+)/$',confirm),
        url(r'^invite/$',invite),
        url(r'^password_change/$',password_change,
            {'template_name':'usercenter/password_change.html',
                'post_change_redirect':'/usercenter/password_change/done/'}),
        url(r'^password_change/done/$',password_change_done,
            {'template_name':'usercenter/password_change_done.html'}),
        url(r'^password_reset/$',password_reset,
            {'template_name':'usercenter/password_reset.html'}),
        url(r'^password_reset/done/$', password_reset_done,
            {'template_name':'usercenter/password_reset_done.html'}),
        url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
            {'template_name':'usercenter/password_reset_confirm.html'}),
        url(r'^reset/done/$', password_reset_complete,
            {'template_name':'usercenter/password_reset_complete.html'}),
        )

