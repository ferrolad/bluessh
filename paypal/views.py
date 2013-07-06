# encoding=utf-8
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from utility import baseutil
import datetime
from alipay.models import Transaction
from cart import Cart
from django.shortcuts import render
from paypal.standard.ipn.signals import payment_was_successful
from django.shortcuts import get_object_or_404
from django.conf import settings
from usercenter.views import create_ssh_user
from django.core.mail import mail_admins


@login_required
def checkout(request):
    # 订单号
    out_trade_no = baseutil.time_hash()

    cart = Cart(request)
    # 关闭cart购物车,防止付款之前购物车内内容改变
    cart.cart.checked_out=True
    cart.cart.save()
    # 记录transaction
    now = datetime.datetime.now()
    Transaction.objects.create(out_trade_no=out_trade_no,user=request.user,\
            cart=cart.cart,payed_fee=0,trade_time=now)

   # What you want the button to do.
    paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": (cart.total_fee)/5, # exchange rate is 5
            "item_name": "Bluessh ssh+vpn fee",
            "invoice": out_trade_no, # 本站订单号
            "notify_url": "%s%s" % (settings.SITE_URL, '/paypal/ipn_pengzhao/'),
            "return_url": "%s/usercenter/" % settings.SITE_URL,
            "currency_code":"USD", # 人民币CNY，美元USD
            "charset":"utf-8",
            }

    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    submit_js = "<script>document.forms['paypalsubmit'].submit()</script>"
    return render(request,'usercenter/checkout.html',
                  {'content':paypal_form.render(),'submit_js':submit_js})
# 支付成功的回调函数
def do_business(sender, **kwargs):
    baseutil.well_print('ipn received')
    ipn_obj = sender
    out_trade_no = ipn_obj.invoice # 本站订单号
    total_fee = ipn_obj.mc_gross
    trade = get_object_or_404(Transaction,out_trade_no=out_trade_no)
    # send mail to admin
    mail_content = u"Bluessh有新用户付款成功，用户名为 %s, 付款金额为 $%s"\
                    % (trade.user.username,total_fee)
    mail_admins(u"Bluessh有新用户付款成功",
                mail_content,
                fail_silently=True)
    #创建账单对应的ssh帐号，并保存到UserProduct
    baseutil.well_print("username:%s, total_fee:%s" % (trade.user.username,total_fee))
    create_ssh_user(trade)
# connect signal
payment_was_successful.connect(do_business)

