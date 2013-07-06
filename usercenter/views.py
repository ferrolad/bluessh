#coding=utf-8
from django.http import HttpResponseRedirect
from usercenter.forms import RegForm
from models import *
from utility import mailutil
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utility.sshutil import SSHUtil
from utility import baseutil
from django.shortcuts import render_to_response
import datetime
from django.template import RequestContext


def register(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user_code = UserCode(user=new_user)
            user_code.save()

            sendVerificationEmail(new_user)
            return render_to_response('usercenter/show_info.html',
                                      {'info': "<h3>感谢您的注册，请到您的注册邮箱激活您的帐号</h3>\n\n\
                            <a href='/usercenter/login'>点此登录</a>"})
    else:
        form = RegForm()
    return render_to_response("usercenter/reg.html", {'form': form},
                              context_instance=RequestContext(request)
                              )


def sendVerificationEmail(user):
    '''给指定用户发送验证邮件'''
    to = user.username
    subject = u"BlueSSH帐号激活"
    usercode = UserCode.objects.get(user=user).usercode
    text = u"尊敬的用户:\n\t您好，感谢您注册BlueSSH。\n请点击以下链接激活您的帐号:\n\
            %s/usercenter/confirm/%s/\n\n注意：这是一封系统自动发出的邮件，请勿直接回复。" \
            % (settings.SITE_URL, usercode)
    mailutil.mail_to_one(subject, text, to)


@login_required
def usercenter_home(request):
    product = UserProduct.objects.filter(user=request.user)
    return render_to_response("usercenter/user_home.html",
                              {'product': product},
                              context_instance=RequestContext(request)
                              )


@login_required
def invite(request):
    return render_to_response("usercenter/invite.html",
                              {'content_right': u'<h3>即将上线，敬请期待...</h3>'},
                              context_instance=RequestContext(request)
                              )


def confirm(request, ver_code):
    """处理用户注册后的邮件确认"""
    try:
        user_code = UserCode.objects.get(usercode=ver_code)
        user = user_code.user
        user.is_active = 1
        user.save()
        messages.success(request, u"您的账户已激活,现在可以登录")
        #send mail to admin
        #mail_admins(u"Bluessh有新用户激活成功",
        #                        u"Bluessh有新用户激活成功，用户名为 %s" % user.username,
        #                    fail_silently=True)
        return HttpResponseRedirect("/usercenter/login/")

    except UserCode.DoesNotExist:
        return render_to_response("usercenter/show_info.html",
                                  {'info': "<h3 style='color:red;'>该验证地址无效！！</h3>"})


def create_ssh_user(trade):
    '''创建新的SSH帐号.

    先把创建的SSH用户保存到 UserProduct数据库，再在所有服务器上创建该SSH用户'''
    # 待创建的ssh用户list, 每个元素是tuple(username,pwd,expire)
    ssh_info_list = []
    for item in trade.cart.item_set.all():
        # 创建 N 个SSH帐号
        for i in range(item.quantity):
            up = UserProduct()
            #save一次以获得自增的id值
            up.save()
            ssh_user = "user%04d" % up.id
            ssh_pwd = baseutil.time_hash()[-6:]
            expired_date = baseutil.get_expired_date(item.product.valid_months)
            ssh_info_list.append((ssh_user, ssh_pwd, expired_date))

            #保存到 UserProduct
            up.user = trade.user
            up.product = item.product
            up.sshuser = ssh_user
            up.sshpwd = ssh_pwd
            up.buy_date = datetime.datetime.now()
            up.expired_date = expired_date
            # 2013-03-02 post_save signal将触发创建账号
            up.save()
    #在所有服务器上创建该SSH帐号
    #baseutil.well_print("before create ssh user")
    ssh_util = SSHUtil(trade.user, None, None)
    ssh_util.ssh_create_onall(ssh_info_list)
    #baseutil.well_print("after create ssh user")
