#encoding=utf-8
from utility.models import *
from django.contrib import admin 
from time import strftime

class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('formated_time','subject')
    readonly_fields = ('time','subject','detail','user')

    def formated_time(self,obj):
        return u'%s' % obj.time
    formated_time.short_description="Error time"

class SendEmailAdmin(admin.ModelAdmin):
    list_display = ('time','subject')

    def formated_time(self,obj):
        return u'%s' % obj.time
    formated_time.short_description="send time"

admin.site.register(ErrorLog,ErrorLogAdmin)
admin.site.register(SendEmail,SendEmailAdmin)
