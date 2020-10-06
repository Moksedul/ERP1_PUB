
from django.shortcuts import render
from django.db.models import Sum

from payments.models import Payment
from vouchers.models import BuyVoucher
from organizations.models import Persons
from django.contrib.auth.decorators import login_required
from core.views import buy_total_amount


@login_required()
def payment_report(request):
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
    return render(request, "report/payment_report.html", context)
