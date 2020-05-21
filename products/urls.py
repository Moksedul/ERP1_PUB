from django.urls import path
from .views import ProductListView, add_product, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('add_product', add_product, name='add-product'),
    path('product_list', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete')
]
