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
    sale_form = {}
    if request.method == 'POST':  # If the form has been submitted...
        sale_form = SaleForm(request.POST, prefix="sale")
        # b_form = BForm(request.POST, prefix="b")
        # c_form = CForm(request.POST, prefix="c")
        if sale_form.is_valid():  # All validation rules pass
            print("all validation passed")

    context['form'] = sale_form
    return render(request, 'local_sale/sale_add_form.html', context)
