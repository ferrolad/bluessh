#!/usr/bin/env python2
#coding=utf-8
'''
#=============================================================================
#     FileName: alipay_settings.py
#         Desc: alipay的所有配置都在这里设置
#       Author: GitFree
#        Email: pengzhao.lh@gmail.com
#   LastChange: 2012-03-09 22:24:38
#=============================================================================
'''
SITE_URL = "http://bluessh.com"

#↓↓↓↓↓↓↓↓↓↓ alipay用户基本信息基本信息↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
#合作身份者ID，以2088开头由16位纯数字组成的字符串
partner = ""
#交易安全检验码，由数字和字母组成的32位字符串
key = ""
#签约支付宝账号或卖家支付宝帐户
seller_email = "pengzhao.lh@gmail.com"
#页面跳转同步返回页面文件路径 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
return_url = "%s/usercenter/" % SITE_URL
#服务器通知的页面文件路径 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
notify_url = "%s/alipay/notify/" % SITE_URL
#↑↑↑↑↑↑↑↑↑↑ endof alipay用户基本信息基本信息↑↑↑↑↑↑↑↑↑↑↑↑↑
#字符编码格式 目前支持 gbk 或 utf-8
input_charset = "utf-8"
#签名方式 不需修改
sign_type = "MD5"
#访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
transport = "https"

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓ 请求参数 ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
# 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里
subject = u"BlueSSH 套餐费用"
# 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述里
body = "" #程序自动生成
#商品展示地址，要用http:// 格式的完整路径，不允许加?id=123这类自定义参数
show_url = "%s/content/ssh+vpn/" % SITE_URL
#↑↑↑↑↑↑↑↑↑↑ endof 请求参数↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
