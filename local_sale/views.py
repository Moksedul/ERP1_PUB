from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.generic import ListView, DeleteView
from django.forms import formset_factory, inlineformset_factory

from core.digit2words import d2w
from organizations.models import Persons
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
    form1 = SaleForm(instance=sale)
    ProductFormSet = inlineformset_factory(
                    LocalSale, Product, fields=('name', 'rate', 'weight', 'number_of_bag'), extra=1
                    )
    form2set = ProductFormSet(instance=sale)
    if request.method == 'POST':
        print('in post')
        form1 = SaleForm(request.POST or None, instance=sale)
        form2set = ProductFormSet(request.POST, instance=sale)
        if form1.is_valid():
            print('valid')
            sale = form1.save(commit=False)
            sale.posted_by = request.user
            sale.save()
            if form2set.is_valid():
                form2set.save()
            return redirect('/local_sale_list')
    else:
        form1 = form1
        form2set = form2set

    return render(request, 'local_sale/sale_update_form.html', {'form1': form1, 'form2set': form2set})


@login_required()
def sale_detail(request, pk):
    sale = LocalSale.objects.get(id=pk)
    products = Product.objects.filter(sale_no_id=sale.id)
    product_total = 0

    product_list = {
        'products': []

    }

    for product in products:
        amount = product.rate * product.weight
        product_total += amount
        print(amount)
        key = "products"
        product_list.setdefault(key, [])
        product_list[key].append({
            'name': product.name,
            'rate': product.rate,
            'weight': product.weight,
            'amount': amount,
        })

    if sale.transport_charge_payee == 'CUSTOMER':
        sign_charge = '+'
        voucher_total = product_total + sale.transport_charge
    else:
        sign_charge = '-'
        voucher_total = product_total - sale.transport_charge

    grand_total_amount = voucher_total + sale.previous_due - sale.discount
    in_words = d2w(grand_total_amount)
    context = {
        'sale': sale,
        'products': product_list['products'],
        'grand_total': grand_total_amount,
        'product_total': product_total,
        'sign_charge': sign_charge,
        'voucher_total': voucher_total,
        'in_words': in_words,
    }

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

        voucher_contains = self.request.GET.get('voucher_no')
        if voucher_contains is None:
            voucher_contains = 'Select Voucher'
        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'
        phone_no_contains = self.request.GET.get('phone_no')
        if phone_no_contains is None or phone_no_contains == '':
            phone_no_contains = 'Select Phone No'

        today = now()

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
            vouchers = vouchers.filter(sale_no=voucher_contains)

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
