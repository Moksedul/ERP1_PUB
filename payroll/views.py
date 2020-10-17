from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import EmployeeForm


class EmployeeCreate(LoginRequiredMixin, CreateView):
    form_class = EmployeeForm
    template_name = 'payroll/employee_add'
    success_url =
    def form_valid(self, form):
        return super().form_valid(form)
