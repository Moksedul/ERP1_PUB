from django.contrib import admin
from .models import LC


# Register your models here.
class LCAdmin(admin.ModelAdmin):
    list_display = ('lc_number', 'bank_name', 'opening_date')


admin.site.register(LC, LCAdmin)
