from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Stocks


# Create your views here.
class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stocks
    template_name = 'stocks/stock_add_form.html'
    fields = ('room_no', 'number_of_bag', 'weight',
              'name_of_product', 'product_condition', 'remarks',)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)