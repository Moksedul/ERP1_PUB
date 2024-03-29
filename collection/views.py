from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

import string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.digit2words import d2w
from ledger.views import create_account_ledger, update_account_ledger
from local_sale.models import LocalSale

from .models import Collection
from vouchers.models import SaleVoucher
from django.contrib.auth.decorators import login_required
from challan.models import *
from .forms import CollectionFormSale, CollectionFormLocalSale


def load_sale_vouchers(request):
    name = request.GET.get('name')
    challan = []
    if name != 'company.id':
        challan = Challan.objects.filter(company_name=name)
    vouchers = SaleVoucher.objects.filter(challan_no__in=challan)
    context = {
        'vouchers': vouchers,
    }
    return render(request, 'collections/voucher_dropdown_list_options.html', context)


def load_local_sale_vouchers(request):
    name = request.GET.get('name')
    if name != 'company.id':
        vouchers = LocalSale.objects.filter(buyer_name=name).order_by('sale_no')
    else:
        vouchers = []
    context = {
        'vouchers': vouchers,
    }
    return render(request, 'collections/voucher_dropdown_list_options.html', context)


class CollectionCreateSale(LoginRequiredMixin, CreateView):
    form_class = CollectionFormSale
    template_name = 'collections/collection_form.html'

    def form_valid(self, form):
        form.instance.collected_by = self.request.user
        form.instance.sale_type = 'SALE'
        item = form.save()
        voucher = get_object_or_404(Collection, id=item.pk)
        data = {
            'general_voucher': None,
            'payment_no': None,
            'collection_no': voucher,
            'investment_no': None,
            'bk_payment_no': None,
            'salary_payment': None,
            'date': voucher.collection_date,
            'description': 'From Sale',
            'type': 'C'
        }
        create_account_ledger(data)
        super().form_valid(form=form)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Companies.objects.all()
        context['companies'] = companies
        context['form_name'] = 'Sale Collection'
        context['button_name'] = 'Save'
        context['tittle'] = 'Sale Collection'
        return context


# person creation from Payment form
class PersonCreateCollection(LoginRequiredMixin, CreateView):
    model = Persons
    fields = '__all__'
    template_name = 'organizations/person_add.html'
    success_url = '/collection_list'


class CollectionCreateLocalSale(LoginRequiredMixin, CreateView):
    form_class = CollectionFormLocalSale
    template_name = 'collections/collection_form.html'

    def form_valid(self, form):
        form.instance.collected_by = self.request.user
        form.instance.sale_type = 'LOCAL SALE'
        item = form.save()
        voucher = get_object_or_404(Collection, id=item.pk)
        data = {
            'general_voucher': None,
            'payment_no': None,
            'collection_no': voucher,
            'investment_no': None,
            'bk_payment_no': None,
            'salary_payment': None,
            'description': 'From Sale',
            'type': 'C',
            'date': voucher.collection_date
        }
        create_account_ledger(data)
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Local Sale Collection'
        context['button_name'] = 'Save'
        context['tittle'] = 'Local Sale Collection'
        return context


class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'
    ordering = '-collection_date'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admin = self.request.user.is_staff
        names = Persons.objects.all()
        companies = Companies.objects.all()
        sale_vouchers_selection = SaleVoucher.objects.all()
        local_sale_voucher_selection = LocalSale.objects.all()
        business = Organization.objects.all()

        business_contains = self.request.GET.get('business')
        if business_contains is None:
            business_contains = 'Select Business'

        voucher_contains = self.request.GET.get('voucher_no')
        if voucher_contains is None:
            voucher_contains = 'Select Voucher'
        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'
        company_contains = self.request.GET.get('company_name')
        if company_contains is None or company_contains == '':
            company_contains = 'Select Company'

        voucher_list = {'voucher': []}
        for sale in sale_vouchers_selection:
            key = "voucher"
            voucher_list.setdefault(key, [])
            voucher_list[key].append({'voucher_no': sale.voucher_number})
        for local_sale in local_sale_voucher_selection:
            key = "voucher"
            voucher_list.setdefault(key, [])
            voucher_list[key].append({'voucher_no': local_sale.sale_no})

        context['business'] = business
        context['business_selected'] = business_contains
        context['companies'] = companies
        context['names'] = names
        context['sale_voucher_selection'] = voucher_list['voucher']
        context['voucher_selected'] = voucher_contains
        context['name_selected'] = name_contains
        context['company_selected'] = company_contains
        context['form_name'] = 'Update Sale Collection'
        context['button_name'] = 'Update'
        context['tittle'] = 'Collection List'
        context['admin'] = admin
        return context

    def get_queryset(self):
        sale_vouchers = SaleVoucher.objects.all()
        local_sale_vouchers = LocalSale.objects.all()
        collections = Collection.objects.all().order_by('-collection_date')
        voucher_contains = self.request.GET.get('voucher_no')
        business_contains = self.request.GET.get('business')

        if voucher_contains is None:
            voucher_contains = 'Select Voucher'

        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'

        company_contains = self.request.GET.get('company_name')
        if company_contains is None or company_contains == '':
            company_contains = 'Select Company'

        # checking name from input
        if name_contains != 'Select Name':
            person = Persons.objects.get(person_name=name_contains)
            local_sale_vouchers = local_sale_vouchers.filter(buyer_name=person.id)
            collections = collections.filter(local_sale_voucher_no__in=local_sale_vouchers)

        # checking company from input
        if company_contains != 'Select Company' and company_contains != 'None':
            company = Companies.objects.get(name_of_company=company_contains)
            challan = Challan.objects.filter(company_name=company)
            sale = SaleVoucher.objects.filter(challan_no__in=challan)
            collections = collections.filter(sale_voucher_no__in=sale)

        # checking name from input
        if business_contains != 'Select Business' and business_contains is not None:
            business = Organization.objects.get(name=business_contains)
            challans = Challan.objects.filter(business_name=business.id)
            sale = SaleVoucher.objects.filter(challan_no__in=challans)
            local_sale_vouchers = local_sale_vouchers.filter(business_name=business)
            collections = collections.filter\
                (Q(sale_voucher_no__in=sale) | Q(local_sale_voucher_no__in=local_sale_vouchers))

        # checking voucher number from input
        if voucher_contains != '' and voucher_contains != 'Select Voucher':
            voucher_contains = voucher_contains.split('-')[-1]
            sale_vouchers = sale_vouchers.filter(id=voucher_contains)
            if sale_vouchers:
                collections = collections.filter(sale_voucher_no__in=sale_vouchers)
            else:
                local_sale_vouchers = local_sale_vouchers.filter(id=voucher_contains)
                collections = collections.filter(local_sale_voucher_no__in=local_sale_vouchers)
        collection_final = collections
        return collection_final


class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = 'main/confirm_delete.html'
    success_url = '/collection_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Collection'
        context['cancel_url'] = '/collection_list'
        context['tittle'] = 'Delete Collection'
        return context


class CollectionUpdateViewSale(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionFormSale
    template_name = 'collections/collection_form.html'

    def form_valid(self, form):
        form.instance.collected_by = self.request.user
        item = form.save()
        voucher = get_object_or_404(Collection, id=item.pk)

        data = {
            'date': voucher.collection_date
        }
        update_account_ledger(data, voucher.pk)
        super().form_valid(form=form)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Companies.objects.all()
        s_id = self.object.sale_voucher_no
        ls_id = self.object.local_sale_voucher_no

        if s_id:
            sale = SaleVoucher.objects.get(id=s_id.id)
        else:
            sale = None

        if ls_id:
            local_sale = LocalSale.objects.get(id=ls_id.id)
        else:
            local_sale = None

        if sale:
            company = Companies.objects.get(id=sale.challan_no.company_name.id)
        else:
            company = Companies.objects.get()

        context['collection_no'] = self.object.collection_no
        context['company_selected'] = company
        context['companies'] = companies
        context['form_name'] = 'Update Sale Collection'
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Sale Collection'
        return context


class CollectionUpdateViewLocalSale(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionFormLocalSale
    template_name = 'collections/collection_form.html'

    def form_valid(self, form):
        form.instance.collected_by = self.request.user
        item = form.save()
        voucher = get_object_or_404(Collection, id=item.pk)

        data = {
            'date': voucher.collection_date
        }
        update_account_ledger(data, voucher.pk)
        super().form_valid(form=form)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = ' Update Local Sale Collection'
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Local Sale Collection'
        return context


@login_required()
def collection_details(request, pk):
    collection = Collection.objects.get(id=pk)
    collected_amount_word = string.capwords(d2w(collection.collection_amount))
    context = {
        'collection': collection,
        'collected_amount_word': collected_amount_word,
    }
    return render(request, 'collections/collection_detail.html', context)
