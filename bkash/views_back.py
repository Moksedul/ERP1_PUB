from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from accounts.models import Accounts
from ledger.models import AccountLedger
from ledger.views import create_account_ledger
from organizations.models import Persons
from payments.models import Payment
from vouchers.models import GeneralVoucher
from .forms import TransactionForm, PaymentBkashAgentForm
from .models import BkashAgents, BkashTransaction, PaymentBkashAgent


class BkashAgentCreate(LoginRequiredMixin, CreateView):
    model = BkashAgents
    fields = '__all__'
    template_name = 'bkash/agent_form.html'
    success_url = '/agent_list'


class BkashAgentCreateTransaction(LoginRequiredMixin, CreateView):
    model = BkashAgents
    fields = '__all__'
    template_name = 'bkash/agent_form.html'
    success_url = '/add_transaction'


class BkashAgentUpdate(LoginRequiredMixin, UpdateView):
    model = BkashAgents
    fields = '__all__'
    template_name = 'bkash/agent_form.html'
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
        date = form.cleaned_data['transaction_date']
        ledger_type = ''
        general_voucher = None
        payment_voucher = None
        salary_voucher = None
        description = 'N/A'

        # creating general voucher for transaction
        if t_type == 'GENERAL':
            ledger_type = 'G'
            general_voucher = GeneralVoucher(
                person_name=transaction.payed_to,
                cost_Descriptions=form.cleaned_data['description'],
                cost_amount=form.cleaned_data['transaction_amount'],
                from_account=account,
                transaction=transaction,
                date_added=date
            )
            general_voucher.save()

        # creating payment voucher for transaction
        if t_type == 'PAYMENT':
            ledger_type = 'P'
            payment_voucher = Payment(
                payment_for_person=transaction.payed_to,
                payed_by=transaction.posted_by,
                payment_mode='Bkash',
                payment_amount=form.cleaned_data['transaction_amount'],
                payment_from_account=account,
                transaction=transaction,
                remarks=form.cleaned_data['description'],
                payment_date=date
            )
            payment_voucher.save()

        # # creating payment voucher for transaction
        # if t_type == 'SALARY':
        #     ledger_type = 'SP'
        #     salary_voucher = SalaryPayment(
        #         Employee=transaction.payed_to,
        #         payed_by=transaction.posted_by,
        #         payment_mode='Bkash',
        #         amount=form.cleaned_data['transaction_amount'],
        #         payment_from_account=account,
        #         transaction=transaction,
        #         remarks=form.cleaned_data['description']
        #     )
        #     salary_voucher.save()

        # creating ledger
        data = {
            'general_voucher': general_voucher,
            'payment_no': payment_voucher,
            'collection_no': None,
            'investment_no': None,
            'bk_payment_no': None,
            'salary_payment': salary_voucher,
            'description': description,
            'date': date,
            'type': ledger_type
        }
        create_account_ledger(data)

        return HttpResponseRedirect(self.get_success_url())


class TransactionUpdate(LoginRequiredMixin, UpdateView):
    model = BkashTransaction
    form_class = TransactionForm
    template_name = 'bkash/transaction_form.html'
    success_url = '/transaction_list'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        super().form_valid(form=form)
        transaction = get_object_or_404(BkashTransaction, invoice_no=form.cleaned_data['invoice_no'])
        account = Accounts.objects.get(account_name='BKASH')
        t_type = form.cleaned_data['transaction_type']
        date = form.cleaned_data['transaction_date']
        general_voucher = None
        payment_voucher = None
        salary_voucher = None
        description = 'N/A'
        account_ledger = []

        # updating general voucher for transaction
        if t_type == 'GENERAL':
            general_voucher = GeneralVoucher.objects.get(transaction=transaction)
            general_voucher_new = {
                'person_name': transaction.payed_to,
                'cost_Descriptions': form.cleaned_data['description'],
                'cost_amount': form.cleaned_data['transaction_amount'],
                'from_account': account,
                'transaction': transaction,
                'date_added': date
            }
            general_voucher.__dict__.update(general_voucher_new)
            general_voucher.save()
            description = general_voucher.cost_Descriptions
            account_ledger = AccountLedger.objects.get(general_voucher=general_voucher)

            # updating payment voucher for transaction
        if t_type == 'PAYMENT':
            payment_voucher = Payment.objects.get(transaction=transaction)
            payment_voucher_new = {
                'payment_for_person': transaction.payed_to,
                'payed_by': transaction.posted_by,
                'payment_mode': 'Bkash',
                'payment_amount': form.cleaned_data['transaction_amount'],
                'payment_from_account': account,
                'transaction': transaction,
                'remarks': form.cleaned_data['description'],
                'payment_date': date
            }

            payment_voucher.__dict__.update(payment_voucher_new)
            payment_voucher.save()
            account_ledger = AccountLedger.objects.get(payment_no=payment_voucher)

        # updating ledger
        account_ledger_new = {
            'general_voucher': general_voucher,
            'payment_no': payment_voucher,
            'collection_no': None,
            'investment_no': None,
            'bk_payment_no': None,
            'salary_payment': salary_voucher,
            'description': description,
            'date': date,
        }
        account_ledger.__dict__.update(account_ledger_new)
        account_ledger.save()

        return HttpResponseRedirect(self.get_success_url())


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
            'bk_payment_no': voucher,
            'salary_payment': None,
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
