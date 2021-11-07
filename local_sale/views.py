from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.generic import ListView, DeleteView
from django.forms import formset_factory, inlineformset_factory

from core.digit2words import d2w
from core.views import local_sale_detail_calc
from organizations.models import Persons, Organization
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

    context = {
        'tittle': 'New Local Sale',
        'form1': form1,
        'form2set': form2set
    }

    return render(request, 'local_sale/sale_add_form.html', context=context)


@login_required
def sale_update(request, pk):
    sale = LocalSale.objects.get(pk=pk)
    form1 = SaleForm(instance=sale)
    ProductFormSet = inlineformset_factory(
                    LocalSale, Product, fields=('name', 'rate', 'weight', 'number_of_bag'), extra=1
                    )
    form2set = ProductFormSet(instance=sale)
    if request.method == 'POST':

        form1 = SaleForm(request.POST or None, instance=sale)
        form2set = ProductFormSet(request.POST, instance=sale)
        if form1.is_valid():

            sale = form1.save(commit=False)
            sale.posted_by = request.user
            sale.save()
            if form2set.is_valid():
                form2set.save()
            return redirect('/local_sale_list')
    else:
        form1 = form1
        form2set = form2set

    context = {
        'tittle': 'Local Sale Update',
        'form1': form1,
        'form2set': form2set
    }

    return render(request, 'local_sale/sale_update_form.html', context=context)


@login_required()
def sale_detail(request, pk):
    context = local_sale_detail_calc(pk)

    return render(request, 'local_sale/sale_detail.html', context)


class LocalSaleList(LoginRequiredMixin, ListView):
    model = LocalSale
    template_name = 'local_sale/sale_list.html'
    context_object_name = 'sales'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voucher_selection = LocalSale.objects.all()
        names = Persons.objects.all()
        business_names = Organization.objects.all()

        voucher_contains = self.request.GET.get('voucher_no')
        if voucher_contains is None:
            voucher_contains = 'Select Voucher'
        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'
        phone_no_contains = self.request.GET.get('phone_no')
        if phone_no_contains is None or phone_no_contains == '':
            phone_no_contains = 'Select Phone No'

        business_contains = self.request.GET.get('business')
        if business_contains is None or business_contains == '':
            business_contains = 'Select Business'

        today = now()
        context['business_selected'] = business_contains
        context['business_names'] = business_names
        context['names'] = names
        context['voucher_selected'] = voucher_contains
        context['voucher_selection'] = voucher_selection
        context['name_selected'] = name_contains
        context['phone_no_selected'] = phone_no_contains
        context['tittle'] = 'Local Sale List'
        context['today'] = today.date()
        return context

    def get_queryset(self):
        vouchers = LocalSale.objects.all().order_by('-date')
        order = self.request.GET.get('orderby')
        voucher_contains = self.request.GET.get('voucher_no')
        if voucher_contains is None:
            voucher_contains = 'Select Voucher'
        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'
        phone_no_contains = self.request.GET.get('phone_no')

        if phone_no_contains is None or phone_no_contains == '':
            phone_no_contains = 'Select Phone No'

        # checking name from input
        if name_contains != 'Select Name':
            person = Persons.objects.get(person_name=name_contains)
            vouchers = vouchers.filter(buyer_name=person.id)

        # checking phone no from input
        if phone_no_contains != 'Select Phone No' and phone_no_contains != 'None':
            person = Persons.objects.get(contact_number=phone_no_contains)
            vouchers = vouchers.filter(buyer_name=person.id)

        # checking voucher number from input
        if voucher_contains != '' and voucher_contains != 'Select Voucher':
            voucher_contains = voucher_contains.split('-')[-1]
            vouchers = vouchers.filter(id=voucher_contains)

        business_contains = self.request.GET.get('business')
        if business_contains != 'Select Business' and business_contains is not None:
            business = Organization.objects.get(name=business_contains)
            vouchers = vouchers.filter(business_name=business)

        return vouchers


class LocalSaleDelete(LoginRequiredMixin, DeleteView):
    model = LocalSale
    template_name = 'main/confirm_delete.html'
    success_url = '/local_sale_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Local Sale'
        context['tittle'] = 'Local Sale Delete'
        context['cancel_url'] = '/local_sale_list'
        return context
