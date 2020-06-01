from django.urls import path
from . import views
from .views import (
    StockCreateView

    )

urlpatterns = [
    path('add_stock', StockCreateView.as_view(), name='add-stock'),
    path('report', views.stock_view, name='report'),
    # path('challan/<int:pk>/update', ChallanUpdateView.as_view(), name='challan-update'),
    # path('challan/<int:pk>/delete', ChallanDeleteView.as_view(), name='challan-delete'),

]
