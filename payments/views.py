from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Payment
from accounts.models import Accounts
from .forms import PaymentForm


# Create your views here.
class PaymentCreate(LoginRequiredMixin, CreateView):
    form_class = PaymentForm
    # model = Payment
    template_name = 'payments/payment_add_form.html'
    # fields = '__all__'

    def form_valid(self, form):
        # account = Accounts.objects.get(pk=form.cleaned_data['payment_from_account'].id)
        # amount = form.cleaned_data['payment_amount']
        # remaining_balance = account.remaining_balance
        # new_remaining_balance = amount + remaining_balance
        # account.remaining_balance = new_remaining_balance
        # account.save()
        print('response')
        return super().form_valid(form)


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 5


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_update_form.html'


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    # template_name = 'payments/payment_Detail.html'


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'payments/payment_confirm_delete.html'
    success_url = '/payment_list'