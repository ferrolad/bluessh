#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart


class Transaction(models.Model):
    """Transaction models"""
    out_trade_no = models.CharField(max_length=32)
    user = models.ForeignKey(User)
    cart = models.ForeignKey(Cart)
    payed_fee = models.FloatField(verbose_name=u"总金额")
    trade_time = models.DateTimeField()

    def __unicode__(self):
        return self.out_trade_no
