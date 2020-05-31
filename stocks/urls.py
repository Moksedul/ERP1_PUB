from django.urls import path
from .views import (
    StockCreateView
    )

urlpatterns = [
    path('add_stock', StockCreateView.as_view(), name='add-stock'),
    # path('challan_list', ChallanListView.as_view(), name='challan-list'),
    # path('challan/<int:pk>/update', ChallanUpdateView.as_view(), name='challan-update'),
    # path('challan/<int:pk>/delete', ChallanDeleteView.as_view(), name='challan-delete'),

]
