from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from vouchers.models import GeneralVoucher
from collection.models import Collection


@login_required()
def index(request):
    general_vouchers = GeneralVoucher.objects.all()
    collections = Collection.objects.all()

    ledgers = {

    }

    for voucher in general_vouchers:
        key = "voucher"
        ledgers.setdefault(key, [])
        ledgers[key].append({
            'date': voucher.date_added,
            'voucher_no': voucher.voucher_number,
            'descriptions': voucher.cost_Descriptions,
            'amount': voucher.cost_amount
        })

    context = {
        'ledgers': ledgers['voucher']
    }

    return render(request, 'ledger/ledger.html', context)
