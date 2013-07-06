#encoding=utf-8
from content.models import *
from django.contrib import admin

class LinkContentAdmin(admin.ModelAdmin):
    list_display=('title','link_url')
    list_editable=('link_url',)
    class Media:
        css={'all':('/static/js/KindEditor/themes/default/default.css',)}
        js=('/static/js/KindEditor/kindeditor-min.js',
           '/static/js/KindEditor/lang/zh_CN.js',
           '/static/js/KindEditor/create.js',)

class MenuTabAdmin(admin.ModelAdmin):
    ordering=['-is_display','show_index']
    list_display=('name','show_index','is_display')
    list_editable=('show_index','is_display')

class NoticeAdmin(admin.ModelAdmin):
    ordering=['start_date','end_date']
    list_display=('info','is_shown',)
    list_editable=('is_shown',)

admin.site.register(menu_tab,MenuTabAdmin)
admin.site.register(link_content,LinkContentAdmin)
admin.site.register(Notice,NoticeAdmin)
