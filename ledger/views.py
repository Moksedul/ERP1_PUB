from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from vouchers.models import GeneralVoucher
from collection.models import Collection
from payments.models import Payment


@login_required()
def index(request):
    general_vouchers = GeneralVoucher.objects.all()
    collections = Collection.objects.all()
    payments = Payment.objects.all()

    ledgers = {

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

    def my_function(e):
        return e['date']

    shorting_by_date = ledgers['voucher'].sort(key=my_function, reverse=True)

    context = {
        'shorting_by_date': shorting_by_date,
        'ledgers': ledgers['voucher']
    }

    return render(request, 'ledger/ledger.html', context)
