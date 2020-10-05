from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from accounts.models import Accounts
from ledger.views import create_account_ledger
from organizations.models import Persons
from payments.models import Payment
from vouchers.models import GeneralVoucher
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
        transaction = get_object_or_404(BkashTransaction, invoice_no=form.cleaned_data['invoice_no'])
        account = Accounts.objects.get(account_name='BKASH')
        t_type = form.cleaned_data['transaction_type']

        # creating general voucher for transaction
        if t_type == 'GENERAL':
            general_voucher = GeneralVoucher(
                person_name=transaction.payed_to,
                cost_Descriptions=form.cleaned_data['description'],
                cost_amount=form.cleaned_data['transaction_amount'],
                from_account=account,
                transaction=transaction,
            )
            general_voucher.save()

            # creating ledger for corresponding general voucher
            data = {
                'general_voucher': general_voucher,
                'payment_no': None,
                'collection_no': None,
                'investment_no': None,
                'bk_payment_no': None,
                'description': general_voucher.cost_Descriptions,
                'type': 'G'
            }
            create_account_ledger(data)

            # creating payment voucher for transaction
            if t_type == 'PAYMENT':
                payment_voucher = Payment(
                    payment_for_person=transaction.payed_to,
                    payed_by=transaction.posted_by,
                    payment_mode='Bkash',
                    payment_amount=form.cleaned_data['transaction_amount'],
                    payment_from_account=account,
                    transaction=transaction,
                    remarks=form.cleaned_data['description']
                )
                payment_voucher.save()

                # creating ledger for corresponding payment voucher
                data = {
                    'general_voucher': None,
                    'payment_no': payment_voucher,
                    'collection_no': None,
                    'investment_no': None,
                    'bk_payment_no': None,
                    'description': 'N/A',
                    'type': 'P'
                }
                create_account_ledger(data)

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
        voucher = get_object_or_404(PaymentBkashAgent, payment_no=form.cleaned_data['payment_no'])
        data = {
            'general_voucher': None,
            'payment_no': None,
            'collection_no': None,
            'investment_no': None,
            'description': 'for Bkash Agent Payment',
            'type': 'BK',
            'bk_payment_no': voucher
        }
        create_account_ledger(data)
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