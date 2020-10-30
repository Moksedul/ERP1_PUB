from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from datetime import timedelta, datetime

from accounts.models import Investment, Accounts
from bkash.models import PaymentBkashAgent, BkashAgents
from challan.models import Challan
from ledger.models import AccountLedger
from local_sale.models import LocalSale
from payroll.models import SalaryPayment
from vouchers.models import GeneralVoucher, BuyVoucher, SaleVoucher
from collection.models import Collection
from payments.models import Payment
from organizations.models import Companies, Persons


@login_required()
def ledger(request):
    companies = Companies.objects.all()
    general_vouchers = GeneralVoucher.objects.all()
    collections = Collection.objects.all()
    payments = Payment.objects.all()
    agent_payments = PaymentBkashAgent.objects.all()
    salary_payments = SalaryPayment.objects.all()
    name = request.GET.get('name_contains')
    date1 = request.GET.get('date_from')
    date2 = request.GET.get('date_to')

    if name != '' and name is not None:
        persons = Persons.objects.filter(person_name__contains=name)
        bkash_agents = BkashAgents.objects.filter(agent_name__contains=name)
        p_id = []
        agent_id = []

        for person in persons:
            p_id.append(person.id)
        if p_id:
            payments = payments.filter(payment_for_person_id__in=p_id)
            general_vouchers = general_vouchers.filter(person_name_id__in=p_id)
            collections = Collection.objects.none()
        else:
            payments = Payment.objects.none()
            general_vouchers = GeneralVoucher.objects.none()
            collections = Collection.objects.none()

        for agent in bkash_agents:
            agent_id.append(agent.id)
        if agent_id:
            agent_payments = agent_payments.filter(agent_name_id__in=agent_id)
        else:
            agent_payments = PaymentBkashAgent.objects.none()

    if date1 != '' and date2 != '' and date1 is not None and date2 is not None:
        payments = payments.filter(payment_date__range=[date1, date2])
        collections = collections.filter(collection_date__range=[date1, date2])
        general_vouchers = general_vouchers.filter(date_added__range=[date1, date2])
        agent_payments = agent_payments.filter(payment_date__range=[date1, date2])
    ledgers = {
        'voucher': []

    }

    for voucher in agent_payments:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.payment_date,
            'name': voucher.agent_name,
            'voucher_no': voucher.payment_no + ' Agent Payment ',
            'descriptions': voucher.description,
            'debit_amount': voucher.amount,
            'url1': '#',
            'url2': '#'
        })

    for voucher in general_vouchers:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.date_added,
            'name': voucher.person_name,
            'voucher_no': voucher.voucher_number + ' General Cost',
            'descriptions': voucher.cost_Descriptions,
            'debit_amount': voucher.cost_amount,
            'url1': '#',
            'url2': '#'
        })

    for voucher in salary_payments:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.date,
            'name': voucher.Employee,
            'voucher_no': voucher.month + ' Salary Payment',
            'descriptions': voucher.remarks,
            'debit_amount': voucher.amount,
            'url1': '#',
            'url2': '#'
        })

    for voucher in collections:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.collection_date,
            'name': 'N/A',
            'voucher_no': voucher.collection_no + ' Collection',
            'descriptions': voucher.sale_voucher_no,
            'credit_amount': voucher.collection_amount,
            'url1': '#',
            'url2': '#'
        })

    for voucher in payments:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.payment_date,
            'name': voucher.payment_for_person,
            'voucher_no': voucher.payment_no + ' Payment',
            'descriptions': voucher.voucher_no,
            'debit_amount': voucher.payment_amount,
            'url1': 'payment/' + str(voucher.id) + '/detail',
            'url2': 'buy/' + str(voucher.voucher_no_id) + '/detail'
        })

    if ledgers['voucher']:
        def my_function(e):
            return e['date']

        ledgers['voucher'].sort(key=my_function, reverse=True)

    context = {
        'companies': companies,
        'ledgers': ledgers['voucher']
    }

    return render(request, 'ledger/ledger.html', context)


def create_account_ledger(data):
    account_ledger = AccountLedger(
        general_voucher=data['general_voucher'],
        description=data['description'],
        type=data['type'],
        payment_no=data['payment_no'],
        collection_no=data['collection_no'],
        investment_no=data['investment_no'],
        bk_payment_no=data['bk_payment_no'],
        salary_payment=data['salary_payment'],
    )
    account_ledger.save()
    print(account_ledger)


@login_required()
def account_ledger_report(request):
    date1 = now()
    date2 = now()
    dd = request.POST.get('date')
    selected_account = 14
    account_name_search = request.POST.get('account_name')
    account_ledgers = AccountLedger.objects.all()
    accounts = Accounts.objects.all()
    if account_name_search is not None:
        account_name_id = int(''.join(filter(str.isdigit, account_name_search)))
        selected_account = account_name_id
    account = get_object_or_404(Accounts, pk=selected_account)
    account_balance = 0
    current_day_balance = 0

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
        account_ledgers = account_ledgers.filter(date__range=[date1, date2])

    ledgers = {
        'voucher': []

    }

    for account_ledger in account_ledgers:
        # for agent payment
        if account_ledger.type == 'BK':
            bkash_payment = PaymentBkashAgent.objects.filter(payment_from_account_id=selected_account)
            bkash_payment = bkash_payment.filter(id=account_ledger.bk_payment_no_id)
            for bkash_payment in bkash_payment:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'date': account_ledger.date,
                    'name': bkash_payment.agent_name,
                    'voucher_no': bkash_payment.payment_no,
                    'type': 'Payed for',
                    'descriptions': bkash_payment.transaction_invoice_no,
                    'debit_amount': bkash_payment.amount,
                    'credit_amount': 0,
                    'url1': '/agent_payment_list',
                    'url2': '/agent_payment_list'
                })
        # for general payment
        if account_ledger.type == 'G':
            general_voucher = GeneralVoucher.objects.filter(from_account_id=selected_account)
            general_voucher = general_voucher.filter(id=account_ledger.general_voucher_id)
            for general_voucher in general_voucher:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'date': account_ledger.date,
                    'name': general_voucher.person_name,
                    'voucher_no': general_voucher.voucher_number,
                    'type': 'Cost for',
                    'descriptions': general_voucher.cost_Descriptions,
                    'debit_amount': general_voucher.cost_amount,
                    'credit_amount': 0,
                    'url1': '/general_voucher_list',
                    'url2': '/general_voucher_list'
                })

        # for salary payment
        if account_ledger.type == 'SP':
            salary_payment = SalaryPayment.objects.filter(payment_from_account_id=selected_account)
            salary_payment = salary_payment.filter(id=account_ledger.salary_payment_id)
            for salary_payment in salary_payment:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'date': account_ledger.date,
                    'name': salary_payment.Employee,
                    'voucher_no': salary_payment,
                    'type': 'Cost for',
                    'descriptions': account_ledger.description,
                    'debit_amount': salary_payment.amount,
                    'credit_amount': 0,
                    'url1': '/salary_payment_list',
                    'url2': '/salary_payment_list'
                })

        # for buy payment
        if account_ledger.type == 'P':
            payment = Payment.objects.filter(payment_from_account_id=selected_account)
            payment = payment.filter(pk=account_ledger.payment_no_id)
            for payment in payment:
                if payment.voucher_no_id is not None:
                    buy_voucher = get_object_or_404(BuyVoucher, pk=payment.voucher_no_id)
                    key = "voucher"
                    ledgers.setdefault(key, [])
                    ledgers[key].append({
                        'date': account_ledger.date,
                        'name': buy_voucher.seller_name,
                        'voucher_no': payment.payment_no,
                        'type': 'payment for',
                        'descriptions': account_ledger.description + ' ' + buy_voucher.voucher_number,
                        'debit_amount': payment.payment_amount,
                        'credit_amount': 0,
                        'url1': '/payment/' + str(payment.id) + '/detail',
                        'url2': '/buy/' + str(buy_voucher.id) + '/detail'
                    })
                else:
                    key = "voucher"
                    ledgers.setdefault(key, [])
                    ledgers[key].append({
                        'date': account_ledger.date,
                        'name': payment.payment_for_person,
                        'voucher_no': payment.payment_no,
                        'type': 'payment for',
                        'descriptions': account_ledger.description + '',
                        'debit_amount': payment.payment_amount,
                        'credit_amount': 0,
                        'url1': '/payment/' + str(payment.id) + '/detail',
                        'url2': '#'
                    })
        # for investment
        if account_ledger.type == 'I':
            investment_credit = Investment.objects.filter(investing_to_account_id=selected_account)
            investment_credit = investment_credit.filter(pk=account_ledger.investment_no_id)
            investment_debit = Investment.objects.filter(investing_from_account_id=selected_account)
            investment_debit = investment_debit.filter(pk=account_ledger.investment_no_id)

            for investment in investment_credit:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'date': account_ledger.date,
                    'name': investment.added_by,
                    'voucher_no': '',
                    'type': 'Investment from',
                    'descriptions': account_ledger.description,
                    'debit_amount': 0,
                    'credit_amount': investment.investing_amount,
                    'url1': '#',
                    'url2': '#'
                })
            for investment_debit in investment_debit:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'date': account_ledger.date,
                    'name': investment_debit.added_by,
                    'voucher_no': '',
                    'type': 'Withdraw from',
                    'descriptions': investment_debit.investing_from_account,
                    'debit_amount': investment_debit.investing_amount,
                    'credit_amount': 0,
                    'url1': '#',
                    'url2': '#'
                })

        # for Collection
        if account_ledger.type == 'C':
            collection = Collection.objects.filter(collection_to_account_id=selected_account)
            collection = collection.filter(pk=account_ledger.collection_no_id)

            for collection in collection:
                if collection.sale_type == 'SALE':
                    if collection.sale_voucher_no_id is not None:
                        sale_voucher = get_object_or_404(SaleVoucher, pk=collection.sale_voucher_no_id)
                        challan = get_object_or_404(Challan, pk=sale_voucher.challan_no_id)
                        key = "voucher"
                        ledgers.setdefault(key, [])
                        ledgers[key].append({
                            'date': account_ledger.date,
                            'name': challan.buyer_name,
                            'voucher_no': collection.collection_no,
                            'type': 'Cost',
                            'descriptions': account_ledger.description,
                            'debit_amount': 0,
                            'credit_amount': collection.collection_amount,
                            'url1': '#',
                            'url2': '#'
                        })
                    else:
                        key = "voucher"
                        ledgers.setdefault(key, [])
                        ledgers[key].append({
                            'date': account_ledger.date,
                            'name': collection.collected_from,
                            'voucher_no': collection.collection_no,
                            'type': 'Cost',
                            'descriptions': account_ledger.description,
                            'debit_amount': 0,
                            'credit_amount': collection.collection_amount,
                            'url1': '#',
                            'url2': '#'
                        })

                else:
                    if collection.local_sale_voucher_no is not None:
                        sale_voucher = get_object_or_404(LocalSale, pk=collection.local_sale_voucher_no_id)
                        key = "voucher"
                        ledgers.setdefault(key, [])
                        ledgers[key].append({
                            'date': account_ledger.date,
                            'name': sale_voucher.buyer_name,
                            'voucher_no': collection.collection_no,
                            'type': 'Cost',
                            'descriptions': 'From Local Sale',
                            'debit_amount': 0,
                            'credit_amount': collection.collection_amount,
                            'url1': '#',
                            'url2': '#'
                        })
                    else:
                        key = "voucher"
                        ledgers.setdefault(key, [])
                        ledgers[key].append({
                            'date': account_ledger.date,
                            'name': collection.collected_from,
                            'voucher_no': collection.collection_no,
                            'type': 'Cost',
                            'descriptions': 'From Local Sale',
                            'debit_amount': 0,
                            'credit_amount': collection.collection_amount,
                            'url1': '#',
                            'url2': '#'
                        })

    if ledgers['voucher']:
        def my_function(e):
            return e['date']

        ledgers['voucher'].sort(key=my_function, reverse=False)

    report = {
        'voucher': []
    }

    for item in ledgers['voucher']:
        account_balance = account_balance - item['debit_amount'] + item['credit_amount']
        current_day_balance = current_day_balance + item['credit_amount']
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
            'balance': account_balance,
            'url1': item['url1'],
            'url2': item['url2'],
        })

    date_criteria = 'ALL'
    if date1 is not None and date2 is not None and date1 != '':
        date1 = date1.strftime("%d-%m-%Y")
        date2 = date2.strftime("%d-%m-%Y")
        date_criteria = date1 + ' to ' + date2

    if account.bank_name is not None:
        account_name = str(account.account_name) + str(account.bank_name) + str(account.bank_branch)
    else:
        account_name = account.account_name

    context = {
        'date1': date1,
        'date_criteria': date_criteria,
        'ledgers': report['voucher'],
        'main_balance': current_day_balance,
        'account_name': account_name,
        'accounts': accounts,
        'account_selected_option': account
    }

    return render(request, 'ledger/account_ledger.html', context)
