from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from organizations.models import Persons
from .forms import TransactionForm, PaymentBkashAgentForm
from .models import BkashAgents, BkashTransaction, PaymentBkashAgent


class BkashAgentCreate(LoginRequiredMixin, CreateView):
    model = BkashAgents
    fields = '__all__'
    template_name = 'bkash/agent_add_form.html'
    success_url = '/agent_list'


class BkashAgentCreateTransaction(LoginRequiredMixin, CreateView):
    model = BkashAgents
    fields = '__all__'
    template_name = 'bkash/agent_add_form.html'
    success_url = '/add_transaction'


class BkashAgentUpdate(LoginRequiredMixin, UpdateView):
    model = BkashAgents
    fields = '__all__'
    template_name = 'bkash/agent_add_form.html'
    success_url = '/agent_list'


class BkashAgentList(LoginRequiredMixin, ListView):
    model = BkashAgents
    template_name = 'bkash/agent_list.html'
    context_object_name = 'agents'


class AgentDelete(LoginRequiredMixin, DeleteView):
    model = BkashAgents
    template_name = 'bkash/agent_confirm_delete.html'
    success_url = '/agent_list'


# person creation from Payment form
class PersonCreateBkash(LoginRequiredMixin, CreateView):
    model = Persons
    fields = '__all__'
    template_name = 'organizations/person_add.html'
    success_url = '/add_transaction'


class TransactionCreate(LoginRequiredMixin, CreateView):
    form_class = TransactionForm
    template_name = 'bkash/transaction_form.html'
    success_url = '/transaction_list'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        super().form_valid(form=form)
        return HttpResponseRedirect(self.get_success_url())


class TransactionUpdate(LoginRequiredMixin, UpdateView):
    model = BkashTransaction
    form_class = TransactionForm
    template_name = 'bkash/transaction_form.html'
    success_url = '/transaction_list'


class TransactionDelete(LoginRequiredMixin, DeleteView):
    model = BkashTransaction
    template_name = 'bkash/transaction_confirm_delete.html'
    success_url = '/transaction_list'


class TransactionList(LoginRequiredMixin, ListView):
    model = BkashTransaction
    template_name = 'bkash/transaction_list.html'
    context_object_name = 'transactions'


class AgentPaymentCreate(LoginRequiredMixin, CreateView):
    form_class = PaymentBkashAgentForm
    template_name = 'bkash/agent_payment_form.html'
    success_url = '/agent_payment_list'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        super().form_valid(form=form)
        return HttpResponseRedirect(self.get_success_url())


class AgentPaymentUpdate(LoginRequiredMixin, UpdateView):
    model = PaymentBkashAgent
    form_class = PaymentBkashAgentForm
    template_name = 'bkash/agent_payment_form.html'
    success_url = '/agent_payment_list'


class AgentPaymentList(LoginRequiredMixin, ListView):
    model = PaymentBkashAgent
    template_name = 'bkash/agent_payment_list.html'
    context_object_name = 'payments'


class AgentPaymentDelete(LoginRequiredMixin, DeleteView):
    model = PaymentBkashAgent
    template_name = 'bkash/agent_payment_confirm_delete.html'
    success_url = '/agent_payment_list'