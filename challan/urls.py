from django.urls import path
from .views import (
    ChallanCreateView,
    ChallanUpdateView,
    ChallanListView,
    ChallanDeleteView
    )

urlpatterns = [
    path('add_challan', ChallanCreateView.as_view(), name='add-challan'),
    path('challan_list', ChallanListView.as_view(), name='challan-list'),
    path('challan/<int:pk>/update', ChallanUpdateView.as_view(), name='challan-update'),
    path('challan/<int:pk>/delete', ChallanDeleteView.as_view(), name='challan-delete'),

]
