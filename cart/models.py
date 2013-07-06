#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType


class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)

# added by gitfree
class Discount(models.Model):
    reason = models.CharField(max_length=200)
    percent = models.FloatField(help_text=u'discount percent,like 0.75')
    start_date = models.DateTimeField(verbose_name=_('start date'))
    end_date = models.DateTimeField(verbose_name=_('end date'))
    is_enable = models.BooleanField(default=True)
    def __unicode__(self):
        return self.reason
    class Meta:
        verbose_name = u'折扣'
        verbose_name_plural = u'折扣'


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.SmallIntegerField(verbose_name=_('unit price'))
    # product as generic relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return u''

    def get_total_price(self):
        return self.quantity * self.unit_price
    total_price = property(get_total_price)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)


