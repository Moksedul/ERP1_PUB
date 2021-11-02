from django.contrib import admin
from .models import YardStock


class YardStockAdmin(admin.ModelAdmin):
    list_display = ('voucher_no', 'product', 'weight', 'added_by', 'rate', 'weight_adjustment', 'number_of_bag')


admin.site.register(YardStock, YardStockAdmin)

