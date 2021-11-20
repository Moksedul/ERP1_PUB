from django.urls import path
from . import views
from .views import (
    StockCreateView,
    StockListView,
    StockUpdateView,
    StockDeleteView, FinishedStockCreate, FinishedStockList, FinishedStockUpdate, FinishedStockDelete,

)

urlpatterns = [
    path('add_pre_stock', StockCreateView.as_view(), name='add-pre-stock'),
    path('report', views.stock_view, name='report'),
    path('pre_stock_list', StockListView.as_view(), name='pre-stock-list'),
    path('pre_stock/<int:pk>/update', StockUpdateView.as_view(), name='pre-stock-update'),
    path('pre_stock/<int:pk>/delete', StockDeleteView.as_view(), name='pre-stock-delete'),
    path('add_finished_stock', FinishedStockCreate.as_view(), name='add-finished-stock'),
    path('finished_stock_list', FinishedStockList.as_view(), name='finished-stock-list'),
    path('finished_stock/<int:pk>/update', FinishedStockUpdate.as_view(), name='finished-stock-update'),
    path('finished_stock/<int:pk>/delete', FinishedStockDelete.as_view(), name='finished-stock-delete'),

]
