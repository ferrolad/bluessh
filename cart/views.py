# encoding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render
from cart import Cart
from config.models import Product
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from utility import baseutil
import datetime
from alipay.models import Transaction

@login_required
def cart_get(request):
    cart = Cart(request)
    return render_to_response('usercenter/cart.html',dict(cart = cart),
            context_instance=RequestContext(request))

def cart_add(request, product_name):
    """add one product to the cart"""
    product=Product.objects.get(name=product_name)
    cart=Cart(request)
    cart.add(product, product.price, 1)
    return HttpResponseRedirect('/usercenter/cart/')

# pengzhao 2013-01-21
#def cart_add_product_daily(request, product_name, quantity):
    #"""add product_daily to the cart with quantity."""
    #product = ProductDaily.objects.get(name=product_name)
    #cart = Cart(request)
    #cart.add(product, product.price, quantity)
    ##return HttpResponseRedirect('/usercenter/cart/')
    #return "something to be added later"

def cart_remove(request,product_id):
    product=Product.objects.get(id=product_id)
    cart=Cart(request)
    cart.remove(product)
    return HttpResponseRedirect('/usercenter/cart/')




