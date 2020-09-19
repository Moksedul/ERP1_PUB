from datetime import timedelta, datetime

from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now
from accounts.models import Investment
from bkash.models import PaymentBkashAgent
from collection.models import Collection
from payments.models import Payment
from vouchers.models import BuyVoucher, GeneralVoucher, SaleVoucher, Challan
from daily_cash.models import DailyCash
from organizations.models import Persons
from django.contrib.auth.decorators import login_required
from core.views import buy_total_amount
from django.shortcuts import get_object_or_404


@login_required()
def payment_search(request):
    persons = Persons.objects.all()
    buy_vouchers = BuyVoucher.objects.all()
    buy_voucher = buy_vouchers
    payments_all = Payment.objects.all()
    payments = payments_all
    voucher_contains_query = request.GET.get('voucher_no')
    name_contains_query = request.GET.get('name_contains')
    phone_number_query = request.GET.get('phone_no')
    voucher_total_price = 0
    remaining_amount = 0

    # filter payments by name
    if name_contains_query != '' and name_contains_query is not None:
        persons = persons.filter(person_name__contains=name_contains_query)
        print(persons)
        v_id = []
        for person in persons:
            buy_voucher = buy_vouchers.filter(seller_name=person.id)
            payments = payments_all.filter(payment_for_person_id=person.id)
        for voucher in buy_voucher:
            v_id.append(voucher.id)
        if v_id:
            payments = payments_all.filter(voucher_no_id__in=v_id)

    elif phone_number_query != '' and phone_number_query is not None:
        v_id = []
        person = persons.filter(contact_number=phone_number_query)
        for person in person:
            buy_voucher = buy_vouchers.filter(seller_name=person.id)
        for voucher in buy_voucher:
            v_id.append(voucher.id)
        payments = payments_all.filter(voucher_no_id__in=v_id)

    if voucher_contains_query != 'Select Voucher No' and voucher_contains_query is not None:
        buy_voucher = buy_vouchers.filter(voucher_number=voucher_contains_query)

        for voucher in buy_voucher:
            payments = payments_all.filter(voucher_no_id=voucher.id)

    for voucher in buy_voucher:
        voucher_total_price = voucher_total_price + buy_total_amount(voucher.id)

    total_payed = payments.aggregate(Sum('payment_amount'))
    total_payed = total_payed['payment_amount__sum']

    if total_payed is not None:
        remaining_amount = voucher_total_price - total_payed

    voucher_list = {
        'voucher': []

    }

    for item in buy_voucher:
        key = "voucher"
        voucher_list.setdefault(key, [])
        voucher_list[key].append({
            'date': item.date_added,
            'name': item.seller_name,
            'voucher_no': item.voucher_number,
            'weight': item.weight,
            'rate': item.rate,
            'total_amount': buy_total_amount(item.id),
            'id': item.id
        })

    context = {
        'page_obj': payments,
        'total_payed': total_payed,
        'voucher_total_price': voucher_total_price,
        'remaining_amount': remaining_amount,
        'buy_voucher': voucher_list['voucher'],
        'buy_vouchers': buy_vouchers
    }
    return render(request, "report/buy_report.html", context)


@login_required()
def account_report_index(request):
    return render(request, 'report/accounts_report.html')


@login_required()
def daily_cash_report(request):
    date1 = now()
    date2 = now()
    dd = request.POST.get('date')
    if dd is not None and dd != 'None' and dd != '':
        dd = datetime.strptime(dd, "%d-%m-%Y")
        date1 = dd
        date2 = dd
    daily_cashes = DailyCash.objects.all()
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
        daily_cashes = daily_cashes.filter(date__range=[date1, date2])

    ledgers = {
        'voucher': []

    }

    for daily_cash in daily_cashes:
        # for agent payment
        if daily_cash.type == 'BK':
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
