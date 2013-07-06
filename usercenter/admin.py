#encoding=utf-8
from usercenter.models import *
from django.contrib import admin

class UserProductAdmin(admin.ModelAdmin):
    list_display= ['sshuser','ower','formated_buy_date','formated_expired_date']

    def ower(self,obj):
        return obj.user.username

    def formated_buy_date(self,obj):
        return u'%s' % obj.buy_date

    def formated_expired_date(self,obj):
        return u'%s' % obj.expired_date

    ower.short_description="ower"
    formated_buy_date.short_description="start_date"
    formated_expired_date.short_description="expired_date"

admin.site.register(UserProduct,UserProductAdmin)
