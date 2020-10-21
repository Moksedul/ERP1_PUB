from django.urls import path
from .views import EmployeeCreate, EmployeeUpdate, EmployeeList, EmployeeDelete, attendance_create, delete

urlpatterns = [
    path('add_employee', EmployeeCreate.as_view(), name='add-employee'),
    path('employee_list', EmployeeList.as_view(), name='employee-list'),
    path('employee/<int:pk>/update', EmployeeUpdate.as_view(), name='employee-update'),
    path('employee/<int:pk>/delete', EmployeeDelete.as_view(), name='employee-delete'),
    path('employee/<int:pk>/attendance', attendance_create, name='employee-attendance'),
    path('employee/delete/attendance', delete, name='attendance-delete'),
]
