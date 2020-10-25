from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory, TimeInput
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from core.views import time_difference
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
        'tittle': 'Attendance Update | tecAlong Business',
        'date': day.date
    }
    return render(request, 'payroll/attendance_form.html', context)


@login_required()
def current_day_attendance_update(request):
    day = Day.objects.get(date=now())
    url = '/attendance/' + str(day.id) + '/update'
    return redirect(url)


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


# it is actually Day, all attendance will be deleted to the corresponding day
class AttendanceDelete(LoginRequiredMixin, DeleteView):
    model = Day
    template_name = 'payroll/confirm_delete.html'
    success_url = '/attendance_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Attendance'
        context['cancel_url'] = '/attendance_list'
        return context


@login_required()
def attendance_report(request):
    employees = Employee.objects.all()
    attendances = Attendance.objects.all()
    date1 = now()
    date2 = now()
    dd = request.POST.get('date')
    employee_name = request.POST.get('employee_name')
    if employee_name is not None and employee_name != '---':
        employee_id = int(''.join(filter(str.isdigit, employee_name)))
        employee_selected = get_object_or_404(Employee, pk=employee_id)
        attendances = attendances.filter(employee=employee_selected)
    else:
        employee_selected = '--'

    if dd is not None and dd != 'None' and dd != '':
        dd = datetime.strptime(dd, "%d-%m-%Y")
        date1 = dd
        date2 = dd

    if 'ALL' in request.POST:
        date1 = request.POST.get('date_from')
        date2 = request.POST.get('date_to')
    elif 'Today' in request.POST:
        date1 = now()
        date2 = now()
    elif 'Previous Day' in request.POST:
        date1 = date1 - timedelta(1)
        date2 = date2 - timedelta(1)
    elif 'Next Day' in request.POST:
        date1 = date1 + timedelta(1)
        date2 = date2 + timedelta(1)
    elif request.method == 'POST' and date1 != '' and date2 != '':
        date1 = request.POST.get('date_from')
        date2 = request.POST.get('date_to')
        if date1 is not None and date1 != '':
            date1 = datetime.strptime(date1, "%d-%m-%Y")
            date2 = datetime.strptime(date2, "%d-%m-%Y")

    if date1 != '' and date2 != '' and date1 is not None and date2 is not None:
        days = Day.objects.filter(date__range=[date1, date2])
        d_id = []
        for day in days:
            d_id.append(day.id)
        attendances = attendances.filter(date_id__in=d_id)

    attendances_list = {
        'attendances': []

    }

    for attendance in attendances:
        employee = Employee.objects.get(pk=attendance.employee_id)
        if attendance.present is True:
            time = time_difference(attendance.in_time, attendance.out_time)
            time = time / 3600
            work_hours = round(time, 2)
            status = 'Present'
            status_color = 'background-color:#00254c'
        else:
            work_hours = 0
            status = 'Absent'
            status_color = 'background-color:#FF0000'

        key = "attendances"
        attendances_list.setdefault(key, [])
        attendances_list[key].append({
            'name': employee.employee_name,
            'designation': employee.designation,
            'date': str(attendance.date),
            'in_time': attendance.in_time,
            'out_time': attendance.out_time,
            'status': status,
            'status_color': status_color,
            'work_hour': work_hours
        })

    if attendances_list['attendances']:
        def my_function(e):
            return e['date']

        attendances_list['attendances'].sort(key=my_function, reverse=True)

    date_criteria = 'ALL'
    if date1 is not None and date2 is not None and date1 != '':
        date1 = date1.strftime("%d-%m-%Y")
        date2 = date2.strftime("%d-%m-%Y")
        date_criteria = date1 + ' to ' + date2

    total_work_hour = 0
    employee_payable = 0

    if employee_selected != '--':
        for item in attendances_list['attendances']:
            total_work_hour += item['work_hour']
            total_work_hour = round(total_work_hour, 2)
        employee_payable = total_work_hour * employee_selected.hourly_rate
        print(employee_payable)

    context = {
        'date1': date1,
        'date_criteria': date_criteria,
        'attendances': attendances_list['attendances'],
        'employees': employees,
        'selected_employee': employee_selected,
        'total_work_hour': total_work_hour,
        'employee_payable': employee_payable,
        'tittle': 'Attendance Report | techAlong Business'
    }
    return render(request, "payroll/attendance_report.html", context)
