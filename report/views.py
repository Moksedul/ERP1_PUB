from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.db.models import Sum

from bkash.models import BkashTransaction, PaymentBkashAgent, BkashAgents
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
    names = Persons.objects.all()
    sale_vouchers_selection = SaleVoucher.objects.all()
    local_sale_voucher_selection = LocalSale.objects.all()
    sale_vouchers = SaleVoucher.objects.all()
    local_sale_vouchers = LocalSale.objects.all()
    collections = Collection.objects.all()
    challan_month = request.GET.get('challan_month')
    if challan_month is None:
        challan_month = 'challan(ex.FS0521)'
    voucher_contains = request.GET.get('voucher_no')
    if voucher_contains is None:
        voucher_contains = 'Select Voucher'
    name_contains = request.GET.get('name')
    if name_contains is None:
        name_contains = 'Select Name'
    phone_no_contains = request.GET.get('phone_no')

    if phone_no_contains is None or phone_no_contains == '':
        phone_no_contains = 'Select Phone No'

    total_receivable = 0
    voucher_list = {
        'voucher': []

    }
    for sale in sale_vouchers_selection:
        key = "voucher"
        voucher_list.setdefault(key, [])
        voucher_list[key].append({
            'voucher_no': sale.voucher_number
        })
    for local_sale in local_sale_voucher_selection:
        key = "voucher"
        voucher_list.setdefault(key, [])
        voucher_list[key].append({
            'voucher_no': local_sale.sale_no
        })

    sale_list = {
        'voucher': []
    }

    # checking challan month
    if challan_month != 'challan(ex.FS0521)' and challan_month is not None:
        challan = Challan.objects.filter(challan_serial__contains=challan_month)
        sale_vouchers = sale_vouchers.filter(challan_no__in=challan)
        local_sale_vouchers = local_sale_vouchers.none()
        collections = collections.filter(sale_voucher_no__in=sale_vouchers)
        print('hit')

    # checking name from input
    if name_contains != 'Select Name':
        person = Persons.objects.get(person_name=name_contains)
        local_sale_vouchers = local_sale_vouchers.filter(buyer_name=person.id)
        collections = collections.filter(local_sale_voucher_no__in=local_sale_vouchers)
        sale_vouchers = sale_vouchers.filter(id=0)

    # checking phone no from input
    if phone_no_contains != 'Select Phone No':
        person = Persons.objects.get(contact_number=phone_no_contains)
        local_sale_vouchers = local_sale_vouchers.filter(buyer_name=person.id)
        collections = collections.filter(local_sale_voucher_no__in=local_sale_vouchers)
        sale_vouchers = sale_vouchers.filter(id=0)

    # checking voucher number from input
    if voucher_contains != '' and voucher_contains != 'Select Voucher':
        sale_vouchers = sale_vouchers.filter(voucher_number=voucher_contains)
        if sale_vouchers:
            local_sale_vouchers = LocalSale.objects.none()
            v_id = []
            for voucher in sale_vouchers:
                v_id.append(voucher.id)
            collections = collections.filter(sale_voucher_no_id__in=v_id)
        else:
            sale_vouchers = SaleVoucher.objects.none()
            local_sale_vouchers = local_sale_vouchers.filter(sale_no=voucher_contains)
            v_id = []
            for voucher in local_sale_vouchers:
                v_id.append(voucher.id)
            collections = collections.filter(local_sale_voucher_no_id__in=v_id)

    # sale voucher list
    for voucher in sale_vouchers:
        challan = Challan.objects.get(id=voucher.challan_no.id)
        total_amount = sale_total_amount(voucher.id)
        total_receivable += total_amount

        key = "voucher"
        sale_list.setdefault(key, [])
        sale_list[key].append({
            'date': voucher.date_added,
            'name': challan.company_name,
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
    else:
        collection_due = total_receivable
        total_collected = 0
    context = {
        'challan_month': challan_month,
        'collections': collections,
        'vouchers': sale_list['voucher'],
        'total_collected': round(total_collected, 2),
        'total_receivable': round(total_receivable, 2),
        'collection_due': round(collection_due, 2),
        'sale_voucher_selection': voucher_list['voucher'],
        'voucher_selected': voucher_contains,
        'names': names,
        'name_selected': name_contains,
        'phone_no_selected': phone_no_contains
    }
    return render(request, "report/collection_report.html", context)


@login_required()
def bkash_report(request):
    agent_names = BkashAgents.objects.all()
    bkash_transactions = BkashTransaction.objects.all()
    transaction_selection = bkash_transactions
    agent_payments = PaymentBkashAgent.objects.all()
    voucher_contains = request.GET.get('voucher_no')
    if voucher_contains is None:
        voucher_contains = 'Select Voucher'
    name_contains = request.GET.get('name')
    if name_contains is None or name_contains == '':
        name_contains = 'Select Agent Name'
    phone_no_contains = request.GET.get('phone_no')
    if phone_no_contains is None or phone_no_contains == '':
        phone_no_contains = 'Type Agent Phone No'
    total_payable = 0

    transaction_list = {
        'voucher': []
    }

    # checking name from input
    if name_contains != 'Select Agent Name':
        agent = BkashAgents.objects.get(agent_name=name_contains)
        bkash_transactions = bkash_transactions.filter(agent_name=agent)
        agent_payments = agent_payments.filter(agent_name=agent)

    # checking phone no from input
    if phone_no_contains != 'Type Agent Phone No':
        try:
            agent = BkashAgents.objects.get(agent_number=phone_no_contains)
        except BkashAgents.DoesNotExist:
            context = {
                'transaction_selection': transaction_selection,
                'voucher_selected': voucher_contains,
                'name_typed': name_contains,
                'phone_no_typed': phone_no_contains,
                'message': 'No Data Found with This Phone No'
            }
            return render(request, "report/bkash_report.html", context)

        bkash_transactions = bkash_transactions.filter(agent_name=agent.id)
        agent_payments = agent_payments.filter(agent_name=agent.id)

    # checking voucher number from input
    if voucher_contains != '' and voucher_contains != 'Select Voucher':
        bkash_transactions = BkashTransaction.objects.filter(invoice_no=voucher_contains)
        for bkash_transaction in bkash_transactions:
            agent_payments = agent_payments.filter(transaction_invoice_no=bkash_transaction.id)

    # sale voucher list
    for voucher in bkash_transactions:
        total_payable += voucher.transaction_amount

        key = "voucher"
        transaction_list.setdefault(key, [])
        transaction_list[key].append({
            'date': voucher.transaction_date,
            'name': voucher.agent_name,
            'voucher_no': voucher.invoice_no,
            'total_amount': voucher.transaction_amount,
            'id': voucher.id
        })

    total_payed = agent_payments.aggregate(Sum('amount'))
    total_payed = total_payed['amount__sum']

    if total_payed is not None:
        payment_due = total_payable-total_payed
    else:
        payment_due = total_payable
        total_payed = 0
    context = {
        'payments': agent_payments,
        'vouchers': transaction_list['voucher'],
        'total_payed': total_payed,
        'total_payable': total_payable,
        'payment_due': payment_due,
        'transaction_selection': transaction_selection,
        'voucher_selected': voucher_contains,
        'name_selected': name_contains,
        'phone_no_typed': phone_no_contains,
        'agent_names': agent_names
    }
    return render(request, "report/bkash_report.html", context)
