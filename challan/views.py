from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from organizations.models import Persons, Companies
from .models import Challan
from .forms import ChallanForm


# company creation from Challan form
class CompanyCreateChallan(LoginRequiredMixin, CreateView):
    model = Companies
    fields = '__all__'
    template_name = 'organizations/companies_form.html'
    success_url = '/add_challan'


# person creation from Challan form
class PersonCreateChallan(LoginRequiredMixin, CreateView):
    model = Persons
    fields = '__all__'
    template_name = 'organizations/person_add.html'
    success_url = '/add_challan'


class ChallanCreateView(LoginRequiredMixin, CreateView):
    form_class = ChallanForm
    template_name = 'challan/challan_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'New Challan'
        context['button_name'] = 'Save'
        context['tittle'] = 'New Challan'
        return context


class ChallanUpdateView(LoginRequiredMixin, UpdateView):
    model = Challan
    form_class = ChallanForm
    template_name = 'challan/challan_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Challan'
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Challan'
        return context


class ChallanListView(LoginRequiredMixin, ListView):
    model = Challan
    template_name = 'challan/challan_list.html'
    context_object_name = 'challan'
    paginate_by = 20


class ChallanDeleteView(LoginRequiredMixin, DeleteView):
    model = Challan
    template_name = 'main/confirm_delete.html'
    success_url = '/challan_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Challan'
        context['tittle'] = 'Challan Delete'
        context['cancel_url'] = '/challan_list'
        return context
