from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory, TimeInput
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .forms import EmployeeForm, DayForm, TimeTableForm
from .models import Employee, Day, Attendance, TimeTable


class EmployeeCreate(LoginRequiredMixin, CreateView):
    form_class = EmployeeForm
    template_name = 'payroll/payroll_form.html'
    success_url = 'employee_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Add Employee'
        context['tittle'] = 'Add Employee | techAlong Business'
        return context


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'payroll/payroll_form.html'
    success_url = '/employee_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Employee'
        context['tittle'] = 'Update Employee | techAlong Business'
        return context


class EmployeeList(LoginRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'payroll/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Employees | techAlong Business'
        return context


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'payroll/confirm_delete.html'
    success_url = '/employee_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Employee'
        context['cancel_url'] = '/employee_list'
        return context


class TimetableCreate(LoginRequiredMixin, CreateView):
    form_class = TimeTableForm
    template_name = 'payroll/payroll_form.html'
    success_url = 'timetable_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Add Time Table'
        return context


class TimetableUpdate(LoginRequiredMixin, UpdateView):
    model = TimeTable
    form_class = TimeTableForm
    template_name = 'payroll/payroll_form.html'
    success_url = '/timetable_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Timetable'
        return context


class TimetableList(LoginRequiredMixin, ListView):
    model = TimeTable
    context_object_name = 'timetables'
    template_name = 'payroll/timetable_list.html'


class TimetableDelete(LoginRequiredMixin, DeleteView):
    model = TimeTable
    template_name = 'payroll/confirm_delete.html'
    success_url = '/timetable_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Timetable'
        context['cancel_url'] = '/timetable_list'
        return context


@login_required
def attendance_create(request):
    employees = Employee.objects.all()
    form = DayForm(request.POST or None)

    if form.is_valid():
        day = form.save(commit=False)
        day.save()
        for employee in employees:
            time_table = TimeTable.objects.get(id=employee.time_table_id)
            attendance = Attendance(
                employee=employee,
                date=day,
                in_time=time_table.in_time,
                out_time=time_table.out_time,
            )
            attendance.save()
        return redirect('/attendance_list')
    else:
        form = form

    return render(request, 'payroll/payroll_form.html', {'form': form})


@login_required
def attendance_update(request, pk):
    day = Day.objects.get(pk=pk)
    AttendanceFormSet = inlineformset_factory(
                    Day, Attendance, fields=('employee', 'in_time', 'out_time', 'present'),
                    widgets={
                        'in_time': TimeInput(attrs={'type': 'time'}),
                        'out_time': TimeInput(attrs={'type': 'time'}),
                    },
                    extra=0, can_delete=False,
                    )
    form2set = AttendanceFormSet(instance=day)

    for form in form2set.forms:
        form.fields['employee'].widget.attrs['readonly'] = True
        form.fields['in_time'].widget.attrs.update({'class': ''})

    if request.method == 'POST':
        form2set = AttendanceFormSet(request.POST, instance=day)
        if form2set.is_valid():
            form2set.save()
        return redirect('/attendance_list')
    else:
        form2set = form2set
    context = {
        'form_set': form2set,
        'form_name': 'Attendance Update',
        'tittle': 'Attendance Update | tecAlong Business'
    }
    return render(request, 'payroll/attendance_form.html', context)


# it is actually Day
class AttendanceList(LoginRequiredMixin, ListView):
    model = Day
    context_object_name = 'attendance'
    template_name = 'payroll/attendance_list.html'
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Attendance | techAlong Business'
        return context


def delete(request):
    attendance = Attendance.objects.all()
    print(attendance)
    return render(request, 'payroll/attendance_form.html', )
