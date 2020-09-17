from django.urls import path
from .views import (
    ChallanCreateView,
    ChallanUpdateView,
    ChallanListView,
    ChallanDeleteView,
    PersonCreateChallan,
    CompanyCreateChallan,
    )

urlpatterns = [
    path('add_challan', ChallanCreateView.as_view(), name='add-challan'),
    path('challan/add_person', PersonCreateChallan.as_view(), name='add-person-challan'),
    path('challan/add_company', CompanyCreateChallan.as_view(), name='add-company-challan'),
    path('challan_list', ChallanListView.as_view(), name='challan-list'),
    path('challan/<int:pk>/update', ChallanUpdateView.as_view(), name='challan-update'),
    path('challan/<int:pk>/delete', ChallanDeleteView.as_view(), name='challan-delete'),

]
