from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Payment
from .forms import PaymentForm


# Create your views here.
class PaymentCreate(LoginRequiredMixin, CreateView):
    form_class = PaymentForm
    # model = Payment
    template_name = 'payments/payment_add_form.html'
    # fields = '__all__'
