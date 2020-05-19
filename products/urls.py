from django.urls import path
from . import views
from .views import ProductListView

urlpatterns = [
    path('add_product', views.add_product, name='add-product'),
    path('product_list', ProductListView.as_view(), name='product-list')
]
