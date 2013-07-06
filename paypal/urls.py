#coding=utf-8
from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns=patterns('cart.views',
        url(r'^checkout/$',checkout),       
        # paypal IPN(Instant Payment Notification)
        url(r'^ipn_pengzhao/', include('paypal.standard.ipn.urls')),

    )
