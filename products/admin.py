from django.contrib import admin
from .models import Products


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category')


admin.site.register(Products, ProductAdmin)
