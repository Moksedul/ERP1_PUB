from django.contrib import admin
from .models import PreStock, Store, FinishedStock, ProcessingStock, PostStock


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')


class PreStockAdmin(admin.ModelAdmin):
    list_display = ('voucher_no', 'product', 'weight',
                    'rate_per_kg', 'weight_adjustment',
                    'number_of_bag', 'date_time_stamp', 'last_updated_time',
                    'added_by', 'updated_by')


class ProcessingStockAdmin(admin.ModelAdmin):
    list_display = ('product',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "pre_stocks":
            kwargs["queryset"] = PreStock.objects.filter(added_to_processing_stock=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FinishedStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'weight',
                    'rate_per_kg',
                    'number_of_bag', 'date_time_stamp', 'last_updated_time',
                    'added_by', 'updated_by')


admin.site.register(PreStock, PreStockAdmin)
admin.site.register(ProcessingStock, ProcessingStockAdmin)
admin.site.register(FinishedStock, FinishedStockAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(PostStock)

