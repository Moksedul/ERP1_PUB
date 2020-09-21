from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bkash.models import PaymentBkashAgent
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
        # payments = payments.filter(seller_name__contains=name)
        print(persons)

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
            'voucher_no': voucher.payment_no + ' Agent Payment to ' + str(voucher.agent_name),
            'descriptions': voucher.description,
            'debit_amount': voucher.amount
        })

    for voucher in general_vouchers:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.date_added,
            'voucher_no': voucher.voucher_number + ' General Cost to ' + str(voucher.person_name),
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
        'companies': companies,
        'ledgers': ledgers['voucher']
    }

    return render(request, 'ledger/ledger.html', context)
