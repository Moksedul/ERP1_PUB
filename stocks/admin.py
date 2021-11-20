from django.contrib import admin
from .models import PreStock, Store, FinishedStock


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')


class PreStockAdmin(admin.ModelAdmin):
    list_display = ('voucher_no', 'product', 'weight',
                    'rate_per_kg', 'weight_adjustment',
                    'number_of_bag', 'date_time_stamp', 'last_updated_time',
                    'added_by', 'updated_by')


class FinishedStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'weight',
                    'buying_rate_per_kg', 'processing_cost_per_kg',
                    'number_of_bag', 'date_time_stamp', 'last_updated_time',
                    'added_by', 'updated_by')


admin.site.register(PreStock, PreStockAdmin)
admin.site.register(FinishedStock, FinishedStockAdmin)
admin.site.register(Store, StoreAdmin)

