from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.views import account_balance_calc
from ledger.views import create_account_ledger
from .forms import InvestmentForm
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


def bank_account_list(request):
    accounts = Accounts.objects.all()

    account_list = {
        'account': []

    }

    for account in accounts:
        balance = account_balance_calc(account.id)
        key = "account"
        account_list.setdefault(key, [])
        account_list[key].append({
            'account_name': account.account_name,
            'account_no': account.account_no,
            'bank_branch': str(account.bank_name) + ': ' + str(account.bank_branch),
            'remaining_balance': balance,
            'id': account.id,

        })

    context = {
        'accounts': account_list['account']
    }

    return render(request, 'accounts/bank_account_list.html', context)


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
    form_class = InvestmentForm
    template_name = 'accounts/investment_form.html'
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
            'type': 'I',
            'date': investment_save.date,
            'salary_payment': None
        }
        create_account_ledger(data)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Add Investment'
        context['tittle'] = 'Add Investment'
        context['button_name'] = 'Save'
        return context


class InvestmentList(LoginRequiredMixin, ListView):
    model = Investment
    template_name = 'accounts/investment_list.html'
    context_object_name = 'investments'
    ordering = ['-date_added']
    paginate_by = 20


class InvestmentDelete(LoginRequiredMixin, DeleteView):
    model = Investment
    template_name = 'main/confirm_delete.html'
    success_url = '/investment_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Investment'
        context['cancel_url'] = '/investment_list'
        context['tittle'] = 'Investment Delete'

        return context


class InvestmentUpdate(LoginRequiredMixin, UpdateView):
    model = Investment
    form_class = InvestmentForm
    template_name = 'accounts/investment_form.html'
    success_url = '/investment_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Investment Update'
        context['button_name'] = 'Update'
        context['tittle'] = 'Investment Update'
        return context