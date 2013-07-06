#encoding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from utility.mailutil import mail_to_list
from django.contrib.auth.models import User
from utility.baseutil import well_print

class ErrorLog(models.Model):
    time=models.DateTimeField()
    subject=models.CharField(max_length=50)
    detail=models.TextField()
    user=models.ForeignKey(User,null=True)
    def __unicode__(self):
        return u'%s' % self.time

class SendEmail(models.Model):
    receivers = models.CharField(max_length=2000,
            help_text=u'收件人列表，多个收件人用逗号隔开，ALL表示所有用户')
    subject = models.CharField(max_length=2000)
    content = models.TextField()
    time = models.DateTimeField(auto_now=True)
    confirm = models.BooleanField(default=False,help_text=u'确认是否发送')

def send_mail_post_save(sender,instance,**kwargs):
    """
        SendMail post_save signal callback
    """
    if instance.confirm:
        subject = instance.subject
        content = instance.content
        rev_list = []
        if instance.receivers == 'ALL': #群发所有用户
            for user in User.objects.all():
                rev_list.append(user.email)
        else : #群发指定用户
            rev_list = instance.receivers.split(',')
        #well_print(rev_list)
        #well_print(subject)
        #well_print(content)
        mail_to_list(subject,content,rev_list)
        well_print('send mail done')
signals.post_save.connect(send_mail_post_save,sender=SendEmail)
