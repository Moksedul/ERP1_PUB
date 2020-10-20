from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .forms import EmployeeForm, AttendanceForm
from .models import Employee


class EmployeeCreate(LoginRequiredMixin, CreateView):
    form_class = EmployeeForm
    template_name = 'payroll/employee_form.html'
    success_url = 'employee_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Add New Employee'
        return context


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'payroll/employee_form.html'
    success_url = '/employee_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Employee'
        return context


class EmployeeList(LoginRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'payroll/employee_list.html'


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'payroll/employee_confirm_delete.html'
    success_url = '/employee_list'


@login_required
def attendance_create(request):
    employee = Employee.objects.all()
    attendance_set = formset_factory(AttendanceForm, extra=employee.count())
    print(attendance_set)
    form_set = attendance_set(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form_set.is_valid():
            for form in form_set:
                attendance = form.save(commit=False)
                attendance.save()
            return redirect('/employee_list')
    else:
        form_set = attendance_set
    form_set.forms[-1].fields['date'].required = False
    return render(request, 'payroll/attendance_form.html', {'form_set': form_set, 'form_name': 'Attendance'})
