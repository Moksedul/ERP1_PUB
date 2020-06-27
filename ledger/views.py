from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from vouchers.models import GeneralVoucher


@login_required()
def index(request):
    general_vouchers = GeneralVoucher.objects.all()
    ledger = {

    }
    context = {
        'general_vouchers': general_vouchers
    }
    return render(request, 'ledger/ledger.html', context)
