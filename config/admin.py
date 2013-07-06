from config.models import *
from django.contrib import admin

class EmailContentAdmin(admin.ModelAdmin):
    readonly_fields=('counter',)

class SSHServerAdmin(admin.ModelAdmin):
    list_display = ('address','is_active')
    list_editable = ('is_active',)

admin.site.register(Product)
admin.site.register(SSHServer,SSHServerAdmin)
admin.site.register(EmailContent,EmailContentAdmin)
