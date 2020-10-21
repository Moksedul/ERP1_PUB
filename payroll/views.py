from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .forms import EmployeeForm, AttendanceForm
from .models import Employee, Day, Attendance


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
def attendance_create(request, pk):
    day = Day.objects.get(pk=pk)
    AttendanceFormSet = inlineformset_factory(
                    Day, Attendance, fields=('employee', 'in_time', 'out_time', 'present'), extra=1
                    )
    form2set = AttendanceFormSet(instance=day)
    if request.method == 'POST':
        print('in post')
        form2set = AttendanceFormSet(request.POST, instance=day)
        print('valid')
        if form2set.is_valid():
            form2set.save()
        return redirect('/local_sale_list')
    else:
        form2set = form2set

    return render(request, 'payroll/attendance_form.html', {'form2set': form2set})


def delete(request):
    attendance = Attendance.objects.all()
    print(attendance)
    return render(request, 'payroll/attendance_form.html', )
