#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
import time
import hashlib
from config.models import Product
from django.db.models import signals
from django.dispatch import receiver
from utility.sshutil import SSHUtil
from time import sleep


class UserCode(models.Model):
    user = models.ForeignKey(User)
    usercode = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        #生成用户的hash验证码
        hash = hashlib.md5()
        hash.update(str(time.time()))
        self.usercode = hash.hexdigest()
        super(UserCode, self).save(*args, **kwargs)


class UserProduct(models.Model):
    user = models.ForeignKey(User, null=True)
    product = models.ForeignKey(Product, null=True)
    sshuser = models.CharField(max_length=30)
    sshpwd = models.CharField(max_length=30)
    buy_date = models.DateTimeField(null=True)
    expired_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.sshuser


# gitfree bug:2012-09-23
# added 'dispatch_uid' to void post_save triger twice
# gitfree 2013-03-03
# all account can triger post_save
@receiver(signals.post_save, sender=UserProduct, dispatch_uid='usercenter.Usercenter.post_save')
def userproduct_post_save(sender, instance, created, **kwargs):
    """create ssh user at every ssh server ,
       when add ssh user or change ssh user.
    """
    sshuser = instance.sshuser
    sshpwd = instance.sshpwd
    expired_date = instance.expired_date

    if created:  # new created
        if sshuser and sshpwd and expired_date:  # not up.save() for getting UserProduct id
            # create new ssh on all ssh servers
            ssh_util = SSHUtil(instance.user)
            ssh_info_list = [(sshuser, sshpwd, expired_date)]
            ssh_util.ssh_create_onall(ssh_info_list)
    else:  # not created
        #change ssh password on all ssh servers
        ssh_util = SSHUtil(instance.user)
        if sshuser and sshpwd:  # change password
            ssh_util.ssh_change_pwd_onall(sshuser, sshpwd)
        if expired_date:  # change expired date
            ssh_util.ssh_change_expire_onall(sshuser, expired_date)


@receiver(signals.post_delete, sender=UserProduct, dispatch_uid='usercenter.Usercenter.post_delete')
def userproduct_post_delete(sender, instance, **kwargs):
    """delete ssh user at all ssh-server ,
       when delete ssh user at admin site.
    """
    sshuser = instance.sshuser
    #create ssh on all ssh server
    ssh_util = SSHUtil(instance.user)
    ssh_util.ssh_delete_onall(sshuser)
    # sleep for the situation delete more than 1 account at one time
    sleep(2)
