from django.urls import path
from .views import add_organizations

urlpatterns = [
    path('add_organizations', add_organizations, name='add-organizations'),
    # path('product_list', ProductListView.as_view(), name='product-list'),
    # path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    # path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete')
]
