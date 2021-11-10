from django.contrib import admin
from .models import Stock, Store


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')


class StockAdmin(admin.ModelAdmin):
    list_display = ('voucher_no', 'product', 'weight', 'added_by', 'rate', 'weight_adjustment', 'number_of_bag')


admin.site.register(Stock, StockAdmin)
admin.site.register(Store, StoreAdmin)

