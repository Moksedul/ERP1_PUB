from django.urls import path
from . import views
from .views import (
    StockCreateView,
    StockListView,
    StockUpdateView,
    StockDeleteView,
    RoomCreateView,
    RoomListView,
    RoomUpdateView,
    RoomDeleteView

    )

urlpatterns = [
    path('add_stock', StockCreateView.as_view(), name='add-stock'),
    path('report', views.stock_view, name='report'),
    path('stock_list', StockListView.as_view(), name='stock-list'),
    path('stock/<int:pk>/update', StockUpdateView.as_view(), name='stock-update'),
    path('stock/<int:pk>/delete', StockDeleteView.as_view(), name='stock-delete'),
    path('add_room', RoomCreateView.as_view(), name='add-room'),
    path('room_list', RoomListView.as_view(), name='room-list'),
    path('room/<int:pk>/update', RoomUpdateView.as_view(), name='room-update'),
    path('room/<int:pk>/delete', RoomDeleteView.as_view(), name='room-delete'),

]
