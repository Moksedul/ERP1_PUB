from django.urls import path
from . import views
from .views import (
    StockCreateView,
    StockListView,
    StockUpdateView,
    StockDeleteView, FinishedStockCreate, FinishedStockList, FinishedStockUpdate, FinishedStockDelete,
    ProcessingStockCreate, ProcessingStockList, ProcessingStockUpdate, ProcessingStockDelete,
    processing_stock_mess_creation,

)

urlpatterns = [
    path('add_pre_stock', StockCreateView.as_view(), name='add-pre-stock'),
    path('report', views.stock_view, name='report'),
    path('pre_stock_list', StockListView.as_view(), name='pre-stock-list'),
    path('pre_stock/<int:pk>/update', StockUpdateView.as_view(), name='pre-stock-update'),
    path('pre_stock/<int:pk>/delete', StockDeleteView.as_view(), name='pre-stock-delete'),
    path('add_processing_stock', ProcessingStockCreate.as_view(), name='add-processing-stock'),
    path('processing_stock_mess_creation', processing_stock_mess_creation, name='processing-stock-mess-creation'),
    path('stock_processing_list', ProcessingStockList.as_view(), name='processing-stock-list'),
    path('stock_processing/<int:pk>/update', ProcessingStockUpdate.as_view(), name='processing-stock-update'),
    path('stock_processing/<int:pk>/delete', ProcessingStockDelete.as_view(), name='processing-stock-delete'),
    path('add_finished_stock', FinishedStockCreate.as_view(), name='add-finished-stock'),
    path('finished_stock_list', FinishedStockList.as_view(), name='finished-stock-list'),
    path('finished_stock/<int:pk>/update', FinishedStockUpdate.as_view(), name='finished-stock-update'),
    path('finished_stock/<int:pk>/delete', FinishedStockDelete.as_view(), name='finished-stock-delete'),

]
