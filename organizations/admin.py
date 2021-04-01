from django.contrib import admin
from .models import Companies, Persons, Bank

# Register your models here.
admin.site.register(Companies)
admin.site.register(Persons)
admin.site.register(Bank)
