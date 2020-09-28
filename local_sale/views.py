from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import LocalSale, Product


# Create your views here.
class SaleForm(ModelForm):
    class Meta:
        model = LocalSale
        fields = '__all__'


def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account Has Been Created ! You can now log in.')
            return redirect('#')
    else:
        form = SaleForm()
    return render(request, 'local_sale/sale_add_form.html', {'form': form})
