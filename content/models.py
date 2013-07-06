#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class menu_tab(models.Model):
    name=models.CharField(max_length=20,verbose_name=_('menu'))
    show_index=models.SmallIntegerField()
    is_display=models.BooleanField(u'是否显示该菜单项',default=True)
    link_url=models.CharField(max_length=30)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['show_index']
        verbose_name=u"菜单项"
        verbose_name_plural=u"菜单项"

class link_content(models.Model):
    link_url=models.CharField(u'内容地址',max_length=50,help_text='不包括/content/')
    title=models.CharField(max_length=100)
    content=models.TextField()
    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name=u"页面内容"
        verbose_name_plural=u"页面内容"

# 公告
class Notice(models.Model):
    info = models.CharField(max_length=400)
    start_date = models.DateTimeField(verbose_name=_('start date'))
    end_date = models.DateTimeField(verbose_name=_('end date'))
    is_shown = models.BooleanField(default=True)
    def __unicode__(self):
        return self.info
    class Meta:
        verbose_name = u'公告栏'
        verbose_name_plural = u'公告栏'

class FreeSSH(models.Model):
    username = models.CharField(max_length=20)
    passwd = models.CharField(max_length=10)
    update_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.update_time
