from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import LocalSale, Product


# Create your views here.
class SaleForm(ModelForm):
    class Meta:
        model = LocalSale


def sale_create(request):
    context = {}

    if request.method == 'POST':  # If the form has been submitted...
        sale_form = SaleForm(request.POST, prefix="sale")
        # b_form = BForm(request.POST, prefix="b")
        # c_form = CForm(request.POST, prefix="c")
        if sale_form.is_valid():  # All validation rules pass
            print("all validation passed")

    context['form'] = form
    return render(request, 'vouchers/general_voucher_add_form.html', context)