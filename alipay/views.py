#!/usr/bin/env python
#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from lib.AlipayService import Service
from lib.AlipayNotify import Notify
import datetime
from cart import Cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from models import Transaction
from utility import baseutil
from usercenter.views import create_ssh_user
import alipay_settings  # import alipay user's settings
from django.core.mail import mail_admins

@login_required
def checkout(request):
    #-------------请求参数-------------
    #-------必填参数---------
    #请与贵网站订单系统中的唯一订单号匹配
    out_trade_no = baseutil.time_hash()

    #订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里
    subject = alipay_settings.subject
    #订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述里
    body = alipay_settings.body
    cart = Cart(request)
    for item in cart:
        body = "%s%sx%d+" % (body, item.product.name, item.quantity)
    body = body[:-1]
    #订单总金额，显示在支付宝收银台里的“应付总额里
    #以后添加促销策略，就在这里修改实际应付金额。在页面中传值过来容易被firebug等手动改变
    #记得测试完改回total_fee = cart.total_fee
    #total_fee = 0.01 #测试时使用
    total_fee = cart.total_fee
    #------end of 必填参数------

    #///////扩展功能参数——其他///
    show_url = alipay_settings.show_url
    #-----------endof请求参数----------

    #/////商户自己的业务逻辑/////#
    cart = Cart(request)
    #关闭cart购物车,防止付款之前购物车内内容改变
    cart.cart.checked_out = True
    cart.cart.save()
    #记录transaction
    now = datetime.datetime.now()
    Transaction.objects.create(out_trade_no=out_trade_no, user=request.user,
                               cart=cart.cart, payed_fee=0, trade_time=now)

    #把请求参数打包成数组
    sParaTemp = {}
    sParaTemp["payment_type"] = "1"
    sParaTemp["show_url"] = show_url
    sParaTemp["out_trade_no"] = out_trade_no
    sParaTemp["subject"] = subject
    sParaTemp["body"] = body
    sParaTemp["total_fee"] = total_fee
    #构造即时到帐接口表单提交HTML数据，无需修改
    alipay = Service()
    strHtml = alipay.Create_direct_pay_by_user(sParaTemp)
    return render_to_response("usercenter/checkout.html", {'content': strHtml})

def do_business(request):
    if request.method == 'GET':
        request_method = request.GET
    elif request.method == 'POST':
        request_method = request.POST

    #获取支付宝的通知返回参数，可参考技术文档中服务器异步通知参数列表
    out_trade_no = request_method["out_trade_no"]  # 获取订单号
    total_fee = request_method["total_fee"]

    if request_method["trade_status"] == "TRADE_FINISHED"\
            or request_method["trade_status"] == "TRADE_SUCCESS":
        trade = get_object_or_404(Transaction, out_trade_no=out_trade_no)
        #判断该笔订单是否在商户网站中已经做过处理
        if trade.payed_fee == 0:  # 订单未处理
            #保存实际付款金额，因为促销、打折等会改变实际付款金额
            trade.payed_fee = total_fee
            trade.save()
            # send mail to admin
            mail_admins(u"Bluessh有新用户付款成功",
                        u"Bluessh有新用户付款成功，用户名为 %s, 付款金额为 ￥%s" % (
                            trade.user.username, total_fee),
                        fail_silently=True)
            #创建账单对应的ssh帐号，并保存到UserProduct
            create_ssh_user(trade)

@login_required
def alipay_return(request):
    if request.GET:
        notify = Notify()
        verifyResult = notify.Verify(request.GET,
                                     request.GET["notify_id"], request.GET["sign"])
        if verifyResult:  # 验证成功
            #///请在这里加上商户的业务逻辑//////////
            do_business(request)
            #/////endof 商户业务逻辑////////////////
            return HttpResponse("购买成功！\n")
        else:  # 验证失败
            return HttpResponse("验证失败！")
    else:
        return HttpResponse("无通知参数")

@csrf_exempt
def alipay_notify(request):
    if request.POST:
        notify = Notify()
        verifyResult = notify.Verify(request.POST,
                                     request.POST["notify_id"], request.POST["sign"])
        if verifyResult:  # 验证成功
            #///请在这里加上商户的业务逻辑//////////
            do_business(request)
            #/////endof 商户业务逻辑////////////////
            return HttpResponse("success")  # 返回给支付宝服务器，请勿修改和删除
        else:  # 验证失败
            return HttpResponse("fail")
    else:
        return HttpResponse("无通知参数")
