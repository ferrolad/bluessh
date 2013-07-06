#coding=utf-8
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'sshseller.views.home', name='home'),
        # url(r'^sshseller/', include('sshseller.foo.urls')),
        # Uncomment the admin/doc line below to enable admin documentation:
        #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

        #默认首页
        url(r'^$','views.gotoIndex'),
        url(r'^index/$','views.gotoIndex'),
        url(r'^content/',include('content.urls')),
        url(r'^usercenter/',include('usercenter.urls')),
        url(r'^usercenter/cart/',include('cart.urls')),
        url(r'^alipay/',include('alipay.urls')),
        url(r'^paypal/',include('paypal.urls')),        
        url(r'^admin/tools/',include('admin_tools.urls')),
        url(r'^test/',include('test.urls')),

        # Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),

    )
