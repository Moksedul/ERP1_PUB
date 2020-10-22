from django.urls import path
from .views import EmployeeCreate, EmployeeUpdate, EmployeeList, EmployeeDelete, attendance_create, delete, \
    TimetableList, TimetableCreate, TimetableUpdate, TimetableDelete, AttendanceList, attendance_update

urlpatterns = [
    path('add_employee', EmployeeCreate.as_view(), name='add-employee'),
    path('employee_list', EmployeeList.as_view(), name='employee-list'),
    path('attendance_create', attendance_create, name='attendance-create'),
    path('attendance/<int:pk>/update', attendance_update, name='attendance-update'),
    path('attendance_list', AttendanceList.as_view(), name='attendance-list'),
    path('employee/delete/attendance', delete, name='attendance-delete'),
    path('timetable_create', TimetableCreate.as_view(), name='timetable-create'),
    path('timetable_list', TimetableList.as_view(), name='timetable-list'),
    path('timetable/<int:pk>/update', TimetableUpdate.as_view(), name='timetable-update'),
    path('timetable/<int:pk>/delete', TimetableDelete.as_view(), name='timetable-delete'),
    path('employee/<int:pk>/update', EmployeeUpdate.as_view(), name='employee-update'),
    path('employee/<int:pk>/delete', EmployeeDelete.as_view(), name='employee-delete'),

]
