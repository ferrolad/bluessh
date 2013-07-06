#encoding=utf-8
from django.db import models

class Product(models.Model):
    '''Product payed by month'''
    name=models.CharField(max_length=20,unique=True)
    price=models.SmallIntegerField(help_text='商品单价（单位:元）')
    can_discount=models.BooleanField(help_text='该商品是否可以获得优惠')
    valid_months=models.SmallIntegerField(help_text='可使用月份数')
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['valid_months']

# gitfree 2013-01-21
#class ProductDaily(models.Model):
    #'''Product payed by day'''
    #name = models.CharField(max_length=20, unique=True)
    #price = models.FloatField(help_text='单价（单位:元）')
    #can_discount = models.BooleanField(default=False, help_text='该商品是否可以获得优惠')
    #valid_days = models.SmallIntegerField(help_text='可使用天数')
    #def __unicode__(self):
        #return self.name
    #class Meta:
        #ordering = ['valid_days']

class SSHServer(models.Model):
    address=models.CharField(max_length=50,verbose_name=u"服务器地址")
    port=models.SmallIntegerField(verbose_name=u'端口号')
    admin_user=models.CharField(max_length=50,verbose_name=u'管理员帐号')
    admin_pwd=models.CharField(max_length=50,verbose_name=u'管理员密码')
    description=models.CharField(max_length=100,verbose_name=u"描述信息")
    is_active=models.BooleanField(default=True, verbose_name=u'启用')
    def __unicode__(self):
        return self.description
    class Meta:
        verbose_name=u'SSH服务器设置'
        verbose_name_plural=u'SSH服务器设置'

class EmailContent(models.Model):
    subject=models.CharField(max_length=100,verbose_name=u'邮件主题')
    sender=models.EmailField(max_length=50,verbose_name=u"发件人")
    content=models.TextField(verbose_name=u"邮件内容")
    counter=models.IntegerField(default=0, verbose_name=u"已发送次数")
    def __unicode__(self):
        return self.subject
    class Meta:
        verbose_name=u'邮件内容设置'
        verbose_name_plural=u'邮件内容设置'
