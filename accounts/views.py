from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.decorators import login_required


@login_required()
def home(request):
    return render(request, 'accounts/accounts.html')


class BankAccountCreate(LoginRequiredMixin, CreateView):
    model = Accounts
    template_name = 'accounts/bank_account_add_form.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.remaining_balance = form.cleaned_data['opening_balance']
        return super().form_valid(form)


class BankAccountList(LoginRequiredMixin, ListView):
    model = Accounts
    template_name = 'accounts/bank_account_list.html'
    context_object_name = 'accounts'
    ordering = ['-date_added']
    paginate_by = 5


class BankAccountUpdate(LoginRequiredMixin, UpdateView):
    model = Accounts
    template_name = 'accounts/bank_account_update_form.html'
    fields = '__all__'


class BankAccountDelete(LoginRequiredMixin, DeleteView):
    model = Accounts
    template_name = 'accounts/bank_account_delete.html'
    success_url = '/bank_account_list'


class OtherAccountCreate(LoginRequiredMixin, CreateView):
    model = Accounts
    template_name = 'accounts/other_account_add_form.html'
    fields = ('account_name', 'opening_balance', 'remarks')

    def form_valid(self, form):
        form.instance.remaining_balance = form.cleaned_data['opening_balance']
        return super().form_valid(form)
    success_url = '/other_account_list'


class OtherAccountList(LoginRequiredMixin, ListView):
    model = Accounts
    template_name = 'accounts/other_account_list.html'
    context_object_name = 'accounts'
    ordering = ['-date_added']
    paginate_by = 5


class OtherAccountUpdate(LoginRequiredMixin, UpdateView):
    model = Accounts
    template_name = 'accounts/other_account_update_form.html'
    fields = '__all__'


class OtherAccountDelete(LoginRequiredMixin, DeleteView):
    model = Accounts
    template_name = 'accounts/other_account_delete.html'
    success_url = '/other_account_list'


class InvestmentCreateView(LoginRequiredMixin, CreateView):
    model = Investment
    template_name = 'accounts/investment_add_form.html'
    fields = ('source_of_investment', 'investing_amount', 'investing_to_account', 'remarks',)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        account = Accounts.objects.get(pk=form.cleaned_data['investing_to_account'].id)
        amount = form.cleaned_data['investing_amount']
        remaining_balance = account.remaining_balance
        new_remaining_balance = amount + remaining_balance
        account.remaining_balance = new_remaining_balance
        account.save()
        return super().form_valid(form)


class InvestmentList(LoginRequiredMixin, ListView):
    model = Investment
    template_name = 'accounts/investment_list.html'
    context_object_name = 'investments'
    ordering = ['-date_added']
    paginate_by = 5


@login_required()
def delete_investment(request, pk):
    investment = Investment.objects.get(id=pk)
    account_selected = investment.investing_to_account
    account_db = Accounts.objects.get(id=account_selected.id)
    investment_amount = investment.investing_amount
    remaining_balance_db = account_db.remaining_balance
    account_db.remaining_balance = remaining_balance_db - investment_amount
    if request.method == "POST":
        url = investment.get_absolute_url()
        investment.delete()
        account_db.save()
        return HttpResponseRedirect(url)
    context = {
        'investment': investment,
        'account': account_selected
                }
    return render(request, "accounts/investment_delete.html", context)
