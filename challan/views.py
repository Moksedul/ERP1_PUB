from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Challan


class ChallanCreateView(LoginRequiredMixin, CreateView):
    model = Challan
    template_name = 'challan/challan_add_form.html'
    fields = ('challan_no', 'buyer_name', 'company_name',
              'product_name', 'weight_per_bag', 'number_of_bag', 'number_of_vehicle', 'name_of_driver',
              'vehicle_plate_number', 'date_added', 'remarks',)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class ChallanListView(LoginRequiredMixin, ListView):
    model = Challan
    template_name = 'challan/challan_list.html'
    context_object_name = 'challan'
    paginate_by = 5


class ChallanUpdateView(LoginRequiredMixin, UpdateView):
    model = Challan
    template_name = 'challan/challan_update_form.html'
    fields = '__all__'


class ChallanDeleteView(LoginRequiredMixin, DeleteView):
    model = Challan
    template_name = 'challan/challan_confirm_delete.html'
    success_url = '/challan_list'
