from models import *
from django.contrib import admin

class DiscountAdmin(admin.ModelAdmin):
    ordering=['start_date','end_date']
    list_display=('reason','percent','is_enable',)
    list_editable=('is_enable',)

admin.site.register(Discount,DiscountAdmin)
