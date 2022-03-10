from django.contrib import admin
from .models import BuyVoucher


# Register your models here.
class BuyVoucherAdmin(admin.ModelAdmin):
    list_display = ('voucher_number', 'seller_name', 'date_added')


admin.site.register(BuyVoucher, BuyVoucherAdmin)
