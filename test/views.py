#coding=utf-8
from django.shortcuts import render_to_response
from utility.sshutil import *
from utility.baseutil import *
from utility.mailutil import *
from usercenter.models import UserProduct
from django.contrib.auth.models import User
import datetime
from config.models import Product


def test(request):
    try:
        from fabric.api import settings, env, sudo
        #from fabric.context_managers import settings
    except Exception as ex:
        return render_to_response('empty.html', {'content': ex.message})
    else:
        return render_to_response('empty.html', {'content': "Test OK!!"})


def mail_test(request):
    mail_to_one('test', 'This is a test email from bluessh.com.',
                'pengzhao.lh@gmail.com')
    return render_to_response('empty.html', {'content': 'email has been sended'})


def create_ssh_test(request):
    #在所有服务器上创建SSH帐号
    #ssh_util = SSHUtil(None)
    #ssh_util.ssh_create_onall([('ssh_test', 'ssh_test', get_expired_date(3))])
    #messages.success(request,"create user successfully")
    up = UserProduct()
    up.user = User.objects.get(username='gitfree')

    product = Product.objects.get(name='SSH+VPN一季套餐')
    up.product = product
    up.sshuser = 'ssh_test'
    up.sshpwd = 'ssh_test'
    up.buy_date = datetime.datetime.now()
    up.expired_date = baseutil.get_expired_date(product.valid_months)
    up.save()
    return HttpResponse(' create user successfully! ')


def delete_ssh_test(request):
    #在所有服务器上删除SSH帐号
    ssh_util = SSHUtil(request, 'ssh_test', 'ssh_test')
    ssh_util.ssh_delete_onall()
    return HttpResponse(' delete user successfully! ')
