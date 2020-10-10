from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from daily_cash.views import create_daily_cash
from ledger.views import create_account_ledger
from .models import *
from django.contrib.auth.decorators import login_required


@login_required()
def home(request):
    return render(request, 'accounts/accounts.html')


class BankAccountCreate(LoginRequiredMixin, CreateView):
    model = Accounts
    template_name = 'accounts/account_form.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Add Bank Account'
        return context


class BankAccountList(LoginRequiredMixin, ListView):
    model = Accounts
    template_name = 'accounts/bank_account_list.html'
    context_object_name = 'accounts'
    ordering = ['-date_added']
    paginate_by = 20


class BankAccountUpdate(LoginRequiredMixin, UpdateView):
    model = Accounts
    template_name = 'accounts/account_form.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Bank Account'
        return context


class BankAccountDelete(LoginRequiredMixin, DeleteView):
    model = Accounts
    template_name = 'accounts/account_delete.html'
    success_url = '/bank_account_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Delete Bank Account'
        return context


class OtherAccountCreate(LoginRequiredMixin, CreateView):
    model = Accounts
    template_name = 'accounts/account_form.html'
    fields = ('account_name', 'remarks')
    success_url = '/other_account_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Add Other Account'
        return context


class OtherAccountList(LoginRequiredMixin, ListView):
    model = Accounts
    template_name = 'accounts/other_account_list.html'
    context_object_name = 'accounts'
    ordering = ['-date_added']
    paginate_by = 20


class OtherAccountUpdate(LoginRequiredMixin, UpdateView):
    model = Accounts
    template_name = 'accounts/account_form.html'
    fields = ('account_name', 'remarks')
    success_url = '/other_account_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Other Account'
        return context


class OtherAccountDelete(LoginRequiredMixin, DeleteView):
    model = Accounts
    template_name = 'accounts/account_delete.html'
    success_url = '/other_account_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Delete Other Account'
        return context


class InvestmentCreateView(LoginRequiredMixin, CreateView):
    model = Investment
    template_name = 'accounts/investment_add_form.html'
    fields = ('source_of_investment', 'investing_amount', 'investing_from_account', 'investing_to_account', 'remarks',)
    success_url = '/investment_list'

    def form_valid(self, form):
        form.instance.added_by = self.request.user

        super().form_valid(form=form)  # saving the form
        investment_save = form.save()  # for getting the id of investment just saved
        description = form.cleaned_data['source_of_investment']
        data = {
            'general_voucher': None,
            'payment_no': None,
            'collection_no': None,
            'bk_payment_no': None,
            'investment_no': investment_save,
            'description': description,
            'type': 'I'
        }
        create_account_ledger(data)
        return HttpResponseRedirect(self.get_success_url())


class InvestmentList(LoginRequiredMixin, ListView):
    model = Investment
    template_name = 'accounts/investment_list.html'
    context_object_name = 'investments'
    ordering = ['-date_added']
    paginate_by = 20


@login_required()
def delete_investment(request, pk):
    investment = Investment.objects.get(id=pk)
    if request.method == "POST":
        url = investment.get_absolute_url()
        investment.delete()

        return HttpResponseRedirect(url)
    context = {
        'investment': investment,
        'account': 'n/a'
    }
    return render(request, "accounts/investment_delete.html", context)
