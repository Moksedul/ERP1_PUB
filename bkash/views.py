from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
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


@login_required()
def bkash_ledger_report(request):
    date1 = now()
    date2 = now()
    dd = request.POST.get('date')
    agent_names = BkashAgents.objects.all()
    bkash_transactions = BkashTransaction.objects.all()
    transaction_selection = bkash_transactions
    agent_payments = PaymentBkashAgent.objects.all()
    balance = 0
    total_balance = 0

    if dd is not None and dd != 'None' and dd != '':
        dd = datetime.strptime(dd, "%d-%m-%Y")
        date1 = dd
        date2 = dd

    if 'ALL' in request.POST:
        date1 = request.POST.get('date_from')
        date2 = request.POST.get('date_to')
    elif 'Today' in request.POST:
        date1 = now()
        date2 = now()
    elif 'Previous Day' in request.POST:
        date1 = date1 - timedelta(1)
        date2 = date2 - timedelta(1)
    elif 'Next Day' in request.POST:
        date1 = date1 + timedelta(1)
        date2 = date2 + timedelta(1)
    elif request.method == 'POST' and date1 != '' and date2 != '':
        date1 = request.POST.get('date_from')
        date2 = request.POST.get('date_to')
        if date1 is not None and date1 != '':
            date1 = datetime.strptime(date1, "%d-%m-%Y")
            date2 = datetime.strptime(date2, "%d-%m-%Y")

    if date1 != '' and date2 != '' and date1 is not None and date2 is not None:
        bkash_transactions = bkash_transactions.filter(transaction_date__range=[date1, date2])

    transactions = {
        'voucher': []

    }

    for bkash_transaction in bkash_transactions:
        key = "voucher"
        transactions.setdefault(key, [])
        transactions[key].append({
            'date': bkash_transaction.transaction_date,
            'name': bkash_transaction.agent_name,
            'voucher_no': bkash_payment.payment_no,
            'type': 'Payed for',
            'descriptions': bkash_payment.transaction_invoice_no,
            'debit_amount': bkash_payment.amount,
            'credit_amount': 0,
            'url1': '/agent_payment_list',
            'url2': '/agent_payment_list'
        })

    if ledgers['voucher']:
        def my_function(e):
            return e['date']

        ledgers['voucher'].sort(key=my_function, reverse=False)

    report = {
        'voucher': []
    }

    for item in ledgers['voucher']:
        balance = balance - item['debit_amount'] + item['credit_amount']
        total_balance = total_balance + item['credit_amount']
        key = "voucher"
        report.setdefault(key, [])
        report[key].append({
            'date': item['date'],
            'name': item['name'],
            'voucher_no': item['voucher_no'],
            'type': item['type'],
            'descriptions': item['descriptions'],
            'debit_amount': item['debit_amount'],
            'credit_amount': item['credit_amount'],
            'balance': balance,
            'url1': item['url1'],
            'url2': item['url2'],
        })

    date_criteria = 'ALL'
    if date1 is not None and date2 is not None and date1 != '':
        date1 = date1.strftime("%d-%m-%Y")
        date2 = date2.strftime("%d-%m-%Y")
        date_criteria = date1 + ' to ' + date2


    context = {
        'date1': date1,
        'date_criteria': date_criteria,
        'ledgers': report['voucher'],
        'main_balance': total_balance,
        'account_name': account_name,
        'accounts': accounts,
        'account_selected_option': account
    }

    return render(request, 'bkash/bkash_payment_ledger.html', context)