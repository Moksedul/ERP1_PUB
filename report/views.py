
from django.shortcuts import render
from django.db.models import Sum

from challan.models import Challan
from collection.models import Collection
from local_sale.models import LocalSale
from payments.models import Payment
from vouchers.models import BuyVoucher, SaleVoucher
from organizations.models import Persons
from django.contrib.auth.decorators import login_required
from core.views import buy_total_amount, sale_total_amount, local_sale_total_amount


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


@login_required()
def collection_report(request):
    sale_vouchers_selection = SaleVoucher.objects.all()
    sale_vouchers = SaleVoucher.objects.all()
    local_sale_vouchers = LocalSale.objects.all()
    collections = Collection.objects.all()
    voucher_contains = request.GET.get('voucher_no')
    total_receivable = 0
    collection_due = 0
    sale_list = {
        'voucher': []

    }

    # checking voucher number from input
    if voucher_contains != '' and voucher_contains is not None:
        sale_vouchers = sale_vouchers.filter(voucher_number=voucher_contains)
        for voucher in sale_vouchers:
            collections = collections.filter(sale_voucher_no_id=voucher.id)

    # sale voucher list
    for voucher in sale_vouchers:
        challan = Challan.objects.get(challan_no=voucher.challan_no)
        total_amount = sale_total_amount(voucher.id)
        total_receivable += total_amount

        key = "voucher"
        sale_list.setdefault(key, [])
        sale_list[key].append({
            'date': voucher.date_added,
            'name': challan.buyer_name,
            'voucher_no': voucher.voucher_number,
            'total_amount': total_amount,
            'sale_type': 'Sale',
            'id': voucher.id
        })

    # local sale voucher list
    for voucher in local_sale_vouchers:
        total_amount = local_sale_total_amount(voucher.id)
        total_receivable += total_amount

        key = "voucher"
        sale_list.setdefault(key, [])
        sale_list[key].append({
            'date': voucher.date,
            'name': voucher.buyer_name,
            'voucher_no': voucher.sale_no,
            'total_amount': total_amount,
            'sale_type': 'Local Sale',
            'id': voucher.id
        })

    total_collected = collections.aggregate(Sum('collection_amount'))
    total_collected = total_collected['collection_amount__sum']

    if total_collected is not None:
        collection_due = total_receivable-total_collected

    context = {
        'collections': collections,
        'vouchers': sale_list['voucher'],
        'total_collected': total_collected,
        'total_receivable': total_receivable,
        'collection_due': collection_due,
        'sale_voucher_selection': sale_vouchers_selection,
        'voucher_selected': voucher_contains
    }
    return render(request, "report/collection_report.html", context)
