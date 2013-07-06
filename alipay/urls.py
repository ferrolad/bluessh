#encoding=utf-8

from django.conf.urls.defaults import patterns,include,url
from views import *

urlpatterns=patterns('alipay.views',
        url(r'^checkout/$',checkout),
        url(r'^notify.*/$',alipay_notify),
        url(r'^return.*/$',alipay_return),
    )
