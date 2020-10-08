
from django.shortcuts import render
from django.db.models import Sum

from challan.models import Challan
from collection.models import Collection
from local_sale.models import LocalSale
from payments.models import Payment
from vouchers.models import BuyVoucher, SaleVoucher
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


@login_required()
def collection_report(request):
    sale_vouchers = SaleVoucher.objects.all()
    local_sale_vouchers = LocalSale.objects.all()
    collections = Collection.objects.all()
    voucher_contains = request.GET.get('voucher_no')
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0
    total_collected = 0
    total_receivable = 0
    collection_due = 0

    if voucher_contains != '' and voucher_contains != 'Select Sale No' and voucher_contains is not None:
        sale_voucher = sale_vouchers.filter(voucher_number=voucher_contains)
        for voucher in sale_voucher:
            collections = collections.filter(sale_voucher_no_id=voucher.id)
    else:
        sale_voucher = sale_vouchers

    for voucher in sale_voucher:
        total_collected = collections.filter(sale_voucher_no_id=voucher.id).aggregate(Sum('collection_amount'))
        rate = voucher.rate
        challan = Challan.objects.filter(challan_no=voucher.challan_no)

        for challan in challan:
            pass

        total_weight = challan.weight
        total_amount = rate*total_weight

        if voucher.weight_of_each_bag is not None:
            total_self_weight_of_bag = voucher.weight_of_each_bag * challan.number_of_bag

        if voucher.per_bag_unloading_cost is not None:
            total_unloading_cost = voucher.per_bag_unloading_cost * challan.number_of_bag

        if voucher.measuring_cost_per_kg is not None:
            total_measuring_cost = voucher.measuring_cost_per_kg * total_weight

        weight_after_deduction = total_weight - total_self_weight_of_bag
        total_amount = rate*weight_after_deduction
        total_receivable = total_amount - total_unloading_cost - total_measuring_cost

    if total_collected != 0 and total_collected['collection_amount__sum'] is not None:
        print(total_collected['collection_amount__sum'])
        collection_due = total_receivable-total_collected['collection_amount__sum']

    voucher_list = {
        'voucher': []

    }

    for item in sale_voucher:
        challan = Challan.objects.get(challan_no=item.challan_no)
        key = "voucher"
        voucher_list.setdefault(key, [])
        voucher_list[key].append({
            'date': item.date_added,
            'name': challan.buyer_name,
            'voucher_no': item.voucher_number,
            'total_amount': 'buy_total_amount(item.id)',
            'id': item.id
        })

    voucher_list = {
        'voucher': []

    }

    for item in sale_voucher:
        challan = Challan.objects.get(challan_no=item.challan_no)
        key = "voucher"
        voucher_list.setdefault(key, [])
        voucher_list[key].append({
            'date': item.date_added,
            'name': challan.buyer_name,
            'voucher_no': item.voucher_number,
            'total_amount': 'buy_total_amount(item.id)',
            'id': item.id
        })

    context = {
        'collections': collections,
        'vouchers': voucher_list['voucher'],
        'total_collected': total_collected,
        'total_receivable': total_receivable,
        'collection_due': collection_due,
        'sale_voucher': voucher_contains
    }
    return render(request, "report/collection_report.html", context)