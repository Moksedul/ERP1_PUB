from django.shortcuts import render
from django.db.models import Sum
from accounts.models import Accounts
from collection.models import Collection
from payments.models import Payment
from vouchers.models import BuyVoucher, GeneralVoucher
from organizations.models import Persons
from django.contrib.auth.decorators import login_required
from core.views import buy_total_amount
from django.shortcuts import get_object_or_404


@login_required()
def payment_search(request):
    persons = Persons.objects.all()
    buy_vouchers = BuyVoucher.objects.all()
    buy_voucher = []
    payments_all = Payment.objects.all()
    payments = []
    voucher_contains_query = request.GET.get('voucher_no')
    name_contains_query = request.GET.get('name_contains')
    phone_number_query = request.GET.get('phone_no')
    voucher_total_price = 0
    total_payed = 0
    remaining_amount = 0

    # filter payments by name
    if name_contains_query != '' and name_contains_query is not None:
        persons = persons.filter(person_name__contains=name_contains_query)
        v_id = []
        for person in persons:
            buy_voucher = buy_vouchers.filter(seller_name=person.id)
        for voucher in buy_voucher:
            v_id.append(voucher.id)
        payments = payments_all.filter(voucher_no_id__in=v_id)
        total_payed = payments.aggregate(Sum('payment_amount'))
        total_payed = total_payed['payment_amount__sum']

    elif phone_number_query != '' and phone_number_query is not None:
        v_id = []
        person = persons.filter(contact_number=phone_number_query)
        for person in person:
            buy_voucher = buy_vouchers.filter(seller_name=person.id)
        for voucher in buy_voucher:
            v_id.append(voucher.id)
        payments = payments_all.filter(voucher_no_id__in=v_id)
        total_payed = payments.aggregate(Sum('payment_amount'))
        total_payed = total_payed['payment_amount__sum']

    if voucher_contains_query != '' and voucher_contains_query != 'Select Voucher No':
        buy_voucher = buy_vouchers.filter(voucher_number=voucher_contains_query)

        for voucher in buy_voucher:
            payments = payments_all.filter(voucher_no_id=voucher.id)
            total_payed = payments.aggregate(Sum('payment_amount'))
            total_payed = total_payed['payment_amount__sum']

    for voucher in buy_voucher:
        voucher_total_price = voucher_total_price + buy_total_amount(voucher.id)

    if total_payed is not None:
        remaining_amount = voucher_total_price - total_payed

    context = {
        'page_obj': payments,
        'total_payed': total_payed,
        'voucher_total_price': voucher_total_price,
        'remaining_amount': remaining_amount,
        'buy_voucher': buy_voucher,
        'buy_vouchers': buy_vouchers
    }
    return render(request, "report/buy_report.html", context)


@login_required()
def account_report_index(request):
    return render(request, 'report/accounts_report.html')


@login_required()
def daily_cash_report(request):
    account = get_object_or_404(Accounts, pk=14)
    general_vouchers = GeneralVoucher.objects.filter(from_account=account.id)
    collections = Collection.objects.filter(collection_to_account=account.id)
    payments = Payment.objects.filter(payment_from_account=account.id)

    date1 = request.GET.get('date_from')
    date2 = request.GET.get('date_to')

    if date1 != '' and date2 != '' and date1 is not None and date2 is not None:
        payments = payments.filter(payment_date__range=[date1, date2])
        collections = collections.filter(collection_date__range=[date1, date2])
        general_vouchers = general_vouchers.filter(date_added__range=[date1, date2])
    ledgers = {
        'voucher': []

    }
    for voucher in general_vouchers:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.date_added,
            'voucher_no': voucher.voucher_number + ' General Cost to ' + voucher.person_name,
            'descriptions': voucher.cost_Descriptions,
            'debit_amount': voucher.cost_amount
        })

    for voucher in collections:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.collection_date,
            'voucher_no': voucher.collection_no + ' Collection',
            'descriptions': voucher.sale_voucher_no,
            'credit_amount': voucher.collection_amount
        })

    for voucher in payments:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.payment_date,
            'voucher_no': voucher.payment_no + ' Payment',
            'descriptions': voucher.voucher_no,
            'debit_amount': voucher.payment_amount
        })

    if ledgers['voucher']:
        def my_function(e):
            return e['date']
        ledgers['voucher'].sort(key=my_function, reverse=True)

    context = {
        'ledgers': ledgers['voucher']
    }

    return render(request, 'report/daily_cash_report.html', context)