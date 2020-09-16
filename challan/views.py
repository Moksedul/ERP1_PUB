from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from organizations.models import Persons
from .models import Challan
from .forms import ChallanForm


# person creation from buy form
class PersonCreateChallan(LoginRequiredMixin, CreateView):
    model = Persons
    fields = '__all__'
    template_name = 'organizations/person_add.html'
    success_url = '/add_challan'


class ChallanCreateView(LoginRequiredMixin, CreateView):
    form_class = ChallanForm
    template_name = 'challan/challan_add_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class ChallanListView(LoginRequiredMixin, ListView):
    model = Challan
    template_name = 'challan/challan_list.html'
    context_object_name = 'challan'
    paginate_by = 20


class ChallanUpdateView(LoginRequiredMixin, UpdateView):
    model = Challan
    template_name = 'challan/challan_update_form.html'
    fields = '__all__'


class ChallanDeleteView(LoginRequiredMixin, DeleteView):
    model = Challan
    template_name = 'challan/challan_confirm_delete.html'
    success_url = '/challan_list'
