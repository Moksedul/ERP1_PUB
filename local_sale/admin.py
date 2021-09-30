from django.contrib import admin

from local_sale.models import LocalSale


class LocalSaleAdmin(admin.ModelAdmin):
    list_display = ('sale_no', 'buyer_name',)


admin.site.register(LocalSale, LocalSaleAdmin)
