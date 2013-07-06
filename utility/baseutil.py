#encoding=utf-8
import hashlib,time
from datetime import date
import datetime
# 启用models后会报错
# from models import ErrorLog
from random import randint

def time_hash():
    '''根据当前时间生成hash值'''
    h=hashlib.md5()
    h.update(str(time.time()) + str(randint(1,10000))) 
    return h.hexdigest()

def get_expired_date(months,start_date=date.today()):
    """get expired date after months months"""
    month_days=(31,28,31,30,31,30,31,31,30,31,30,31)
    year=date.today().year
    month=date.today().month
    day=date.today().day
    month2=(month+months)%12 or 12
    year2=year + (month+months-1)/12 
    #gitfree added 2012-11-29 
    #这里原来应该是个笔误，现把month改为month2，修复特定月份天数越界问题
    if day > month_days[month2-1]:
        day = month_days[month2-1]
    return date(year2,month2,day)

def error_log(subject,detail,user=None):
    '''记录异常到数据库'''
    #log=ErrorLog(time=datetime.datetime.now(),subject=subject,\
            #detail=detail,user=user)
    #log.save()

def well_print(content):
    print '\r\n*******************'
    print content
    print '*******************\r\n'
