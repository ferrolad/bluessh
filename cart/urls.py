#coding=utf-8
from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns=patterns('cart.views',
        url(r'^$',cart_get),
        url(r'^add/(?P<product_name>.+)/$',cart_add),
        url(r'^remove/(?P<product_id>.+)/$',cart_remove),

    )
