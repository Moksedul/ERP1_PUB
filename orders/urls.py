from django.urls import path
from .views import (
    OrderCreateView,
    OrderUpdateView,
    OrderListView,
    OrderDeleteView
    )

urlpatterns = [
    path('add_order', OrderCreateView.as_view(), name='add-order'),
    path('order_list', OrderListView.as_view(), name='order-list'),
    path('order/<int:pk>/update', OrderUpdateView.as_view(), name='order-update'),
    path('order/<int:pk>/delete', OrderDeleteView.as_view(), name='order-delete'),

]
