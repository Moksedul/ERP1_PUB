from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from . import forms
from .models import Orders


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Orders
    template_name = 'orders/order_add_form.html'
    fields = ('order_no', 'person_name', 'company_name',
              'product_name', 'total_weight', 'rate_per_kg', 'percentage_of_fotka', 'percentage_of_moisture',
              'delivery_deadline', 'date_ordered', 'order_status', 'remarks',)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class OrderListView(LoginRequiredMixin, ListView):
    model = Orders
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 5


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Orders
    template_name = 'orders/order_update_form.html'
    fields = '__all__'


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Orders
    template_name = 'orders/order_confirm_delete.html'
    success_url = '/order_list'
