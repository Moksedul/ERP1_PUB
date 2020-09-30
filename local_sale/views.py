from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView
from django.forms import formset_factory, inlineformset_factory
from .forms import SaleForm, ProductForm
from .models import LocalSale, Product


@login_required
def sale_create(request):
    form1 = SaleForm(request.POST or None)
    product_set = formset_factory(ProductForm)
    form2set = product_set(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form1.is_valid():
            sale = form1.save(commit=False)
            sale.posted_by = request.user
            sale.save()
            for form in form2set:
                product = form.save(commit=False)
                product.sale_no = sale
                product.save()
            return redirect('/local_sale_list')
    else:
        form1 = SaleForm
        form2set = product_set

    return render(request, 'local_sale/sale_add_form.html', {'form1': form1, 'form2set': form2set})


@login_required
def sale_update(request, pk):
    sale = LocalSale.objects.get(pk=pk)
    product = Product.objects.filter(sale_no_id=sale.id)
    form1 = SaleForm(instance=sale)
    product_set = inlineformset_factory(LocalSale, Product, fields=('name', 'rate', 'weight'))
    form2set = product_set(instance=sale)
    if request.method == 'POST':
        print('in post')
        form1 = SaleForm(request.POST or None, instance=sale)
        product_set = inlineformset_factory(LocalSale, Product, fields=('name', 'rate', 'weight'))
        form2set = product_set(request.POST or None, request.FILES or None)
        if form1.is_valid():
            print('valid')
            sale = form1.save(commit=False)
            sale.posted_by = request.user
            sale.save()
            for form in form2set:
                product = form.save(commit=False)
                product.sale_no = sale
                product.save()
            return redirect('/local_sale_list')
    else:
        form1 = form1
        form2set = form2set

    return render(request, 'local_sale/sale_add_form.html', {'form1': form1, 'form2set': form2set})


def local_sale_detail(request, pk):
    sale = LocalSale.object.get(id=pk)
    products = Product.objects.filter()

class LocalSaleList(LoginRequiredMixin, ListView):
    model = LocalSale
    template_name = 'local_sale/sale_list.html'
    context_object_name = 'sales'
    paginate_by = 20
    ordering = ['-sale_no']


class LocalSaleDelete(LoginRequiredMixin, DeleteView):
    model = LocalSale
    template_name = 'local_sale/sale_delete.html'
    success_url = '/local_sale_list'
