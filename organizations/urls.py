from django.urls import path
from .views import (
    PersonCreateView,
    PersonDeleteView,
    PersonUpdateView,
    PersonListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
    CompanyListView
    )

urlpatterns = [
    path('add_person', PersonCreateView.as_view(), name='add-person'),
    path('person_list', PersonListView.as_view(), name='person-list'),
    path('person/<int:pk>/update', PersonUpdateView.as_view(), name='person-update'),
    path('person/<int:pk>/delete', PersonDeleteView.as_view(), name='person-delete'),
    path('add_company', CompanyCreateView.as_view(), name='add-company'),
    path('company_list', CompanyListView.as_view(), name='company-list'),
    path('company/<int:pk>/update', CompanyUpdateView.as_view(), name='company-update'),
    path('company/<int:pk>/delete', CompanyDeleteView.as_view(), name='company-delete')
]
