from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.decorators import login_required


@login_required()
def home(request):
    return render(request, 'accounts/accounts.html')


class BankAccountCreate(LoginRequiredMixin, CreateView):
    model = BankAccounts
    template_name = 'accounts/bank_account_add_form.html'
    fields = '__all__'


class BankAccountList(LoginRequiredMixin, ListView):
    model = BankAccounts
    template_name = 'accounts/bank_account_list.html'
    context_object_name = 'accounts'
    paginate_by = 5


class BankAccountUpdate(LoginRequiredMixin, UpdateView):
    model = BankAccounts
    template_name = 'accounts/bank_account_update_form.html'
    fields = '__all__'


class BankAccountDelete(LoginRequiredMixin, DeleteView):
    model = BankAccounts
    template_name = 'accounts/bank_account_delete.html'
    success_url = '/bank_account_list'


class OtherAccountCreate(LoginRequiredMixin, CreateView):
    model = OtherAccounts
    template_name = 'accounts/other_account_add_form.html'
    fields = '__all__'


class OtherAccountList(LoginRequiredMixin, ListView):
    model = OtherAccounts
    template_name = 'accounts/other_account_list.html'
    context_object_name = 'accounts'
    paginate_by = 5


class OtherAccountUpdate(LoginRequiredMixin, UpdateView):
    model = OtherAccounts
    template_name = 'accounts/other_account_update_form.html'
    fields = '__all__'


class OtherAccountDelete(LoginRequiredMixin, DeleteView):
    model = OtherAccounts
    template_name = 'accounts/other_account_delete.html'
    success_url = '/other_account_list'


class InvestmentCreateView(LoginRequiredMixin, CreateView):
    model = Investment
    template_name = 'accounts/investment_add_form.html'
    fields = ('source_of_investment', 'investing_amount', 'investing_to_account', 'remarks',)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)