from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DeleteView
from django.forms import formset_factory
from .forms import SaleForm, ProductForm
from .models import LocalSale


class SaleCreate(LoginRequiredMixin, CreateView):
    form_class = SaleForm
    template_name = 'local_sale/sale_add_form.html'
    success_url = '/add_local_sale'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        super().form_valid(form=form)
        print(form)
        return HttpResponseRedirect(self.get_success_url())


def sale_create(request):
    form1 = SaleForm(request.POST or None)
    product_set = formset_factory(ProductForm)
    form2set = product_set(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form1.is_valid():
            sale = form1.save(commit=False)
            # product = form2.save(commit=False)
            sale.posted_by = request.user
            # sale.save()
            # product.sale_no = sale
            # product.save()
            # print(product.id)
            return redirect('/local_sale_list')
    else:
        form1 = SaleForm
        form2set = product_set

    return render(request, 'local_sale/sale_add_form.html', {'form1': form1, 'form2set': form2set})


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