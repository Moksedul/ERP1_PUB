from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from vouchers.models import GeneralVoucher


@login_required()
def index(request):
    general_vouchers = GeneralVoucher.objects.all()
    ledgers = {}

    for voucher in general_vouchers:
        ledgers['voucher_no'] = voucher.voucher_number

    for item in ledgers:
        print(item)
    context = {
        'vouchers': ledgers['voucher_no']
    }

    return render(request, 'ledger/ledger.html', context)
