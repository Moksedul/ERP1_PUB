from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta, datetime
from bkash.models import PaymentBkashAgent, BkashAgents
from ledger.models import AccountLedger
from vouchers.models import GeneralVoucher
from collection.models import Collection
from payments.models import Payment
from organizations.models import Companies, Persons


@login_required()
def index(request):
    companies = Companies.objects.all()
    general_vouchers = GeneralVoucher.objects.all()
    collections = Collection.objects.all()
    payments = Payment.objects.all()
    agent_payments = PaymentBkashAgent.objects.all()
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
    )
    account_ledger.save()
    print(account_ledger)


@login_required()
def account_ledger_report(request):
    date1 = now()
    date2 = now()
    dd = request.POST.get('date')
    if dd is not None and dd != 'None' and dd != '':
        dd = datetime.strptime(dd, "%d-%m-%Y")
        date1 = dd
        date2 = dd
    account_ledgers = AccountLedger.objects.all()
    account_balance = 0
    current_day_balance = 0

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

    for ledger in account_ledgers:
        # for agent payment
        if ledger.type == 'BK':
            bkash_payment = get_object_or_404(PaymentBkashAgent, pk=daily_cash.bk_payment_no_id)
            key = "voucher"
            ledgers.setdefault(key, [])
            ledgers[key].append({
                'date': daily_cash.date,
                'name': bkash_payment.agent_name,
                'voucher_no': daily_cash.bk_payment_no,
                'type': 'Payed for',
                'descriptions': bkash_payment.transaction_invoice_no,
                'debit_amount': bkash_payment.amount,
                'credit_amount': 0,
                'url1': '/agent_payment_list',
                'url2': '/agent_payment_list'
            })
        # for general payment
        if daily_cash.type == 'G':
            general_voucher = get_object_or_404(GeneralVoucher, pk=daily_cash.general_voucher_id)
            key = "voucher"
            ledgers.setdefault(key, [])
            ledgers[key].append({
                'date': daily_cash.date,
                'name': general_voucher.person_name,
                'voucher_no': daily_cash.general_voucher,
                'type': 'Cost for',
                'descriptions': general_voucher.cost_Descriptions,
                'debit_amount': general_voucher.cost_amount,
                'credit_amount': 0,
                'url1': '/general_voucher_list',
                'url2': '/general_voucher_list'
            })
        # for buy payment
        if daily_cash.type == 'P':
            payment_voucher = get_object_or_404(Payment, pk=daily_cash.payment_no_id)
            print(payment_voucher.voucher_no_id)
            if payment_voucher.voucher_no_id is not None:
                buy_voucher = get_object_or_404(BuyVoucher, pk=payment_voucher.voucher_no_id)
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'date': daily_cash.date,
                    'name': buy_voucher.seller_name,
                    'voucher_no': daily_cash.payment_no,
                    'type': 'payment for',
                    'descriptions': daily_cash.description + ' ' + buy_voucher.voucher_number,
                    'debit_amount': payment_voucher.payment_amount,
                    'credit_amount': 0,
                    'url1': '/payment/' + str(payment_voucher.id) + '/detail',
                    'url2': '/buy/' + str(buy_voucher.id) + '/detail'
                })
            else:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'date': daily_cash.date,
                    'name': payment_voucher.payment_for_person,
                    'voucher_no': daily_cash.payment_no,
                    'type': 'payment for',
                    'descriptions': daily_cash.description + '',
                    'debit_amount': payment_voucher.payment_amount,
                    'credit_amount': 0,
                    'url1': '/payment/' + str(payment_voucher.id) + '/detail',
                    'url2': '#'
                })
        # for investment
        if daily_cash.type == 'I':
            investment = get_object_or_404(Investment, pk=daily_cash.investment_no_id)
            key = "voucher"
            ledgers.setdefault(key, [])
            ledgers[key].append({
                'date': daily_cash.date,
                'name': investment.added_by,
                'voucher_no': '',
                'type': 'Investment from',
                'descriptions': daily_cash.description,
                'debit_amount': 0,
                'credit_amount': investment.investing_amount,
                'url1': '#',
                'url2': '#'
            })
        # for Collection
        if daily_cash.type == 'C':
            collection = get_object_or_404(Collection, pk=daily_cash.collection_no_id)
            sale_voucher = get_object_or_404(SaleVoucher, pk=collection.sale_voucher_no_id)
            challan = get_object_or_404(Challan, pk=sale_voucher.challan_no_id)

            key = "voucher"
            ledgers.setdefault(key, [])
            ledgers[key].append({
                'date': daily_cash.date,
                'name': challan.buyer_name,
                'voucher_no': daily_cash.collection_no,
                'type': 'Cost',
                'descriptions': daily_cash.description,
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

    context = {
        'date1': date1,
        'date_criteria': date_criteria,
        'ledgers': report['voucher'],
        'main_balance': current_day_balance
    }

    return render(request, 'report/daily_cash_report.html', context)