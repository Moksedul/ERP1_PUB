from django.urls import path
from django.views.i18n import JavaScriptCatalog
from .views import sale_create

urlpatterns = [
    path('add_local_sale', sale_create, name='add-local-sale'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
