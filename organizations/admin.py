from django.contrib import admin
from .models import Companies, Persons, Bank, Organization

# Register your models here.
admin.site.register(Companies)
admin.site.register(Persons)
admin.site.register(Bank)
admin.site.register(Organization)
