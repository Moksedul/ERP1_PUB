from django.urls import path
from .views import EmployeeCreate

urlpatterns = [
    path('add_employee', EmployeeCreate.as_view(), name='add-employee'),
    # path('employee_list', PersonListView.as_view(), name='employee-list'),
    # path('employee/<int:pk>/update', PersonUpdateView.as_view(), name='employee-update'),
    # path('employee/<int:pk>/delete', PersonDeleteView.as_view(), name='employee-delete'),
]
