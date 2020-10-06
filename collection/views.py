from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
import string
from num2words import num2words
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ledger.views import create_account_ledger
from local_sale.models import LocalSale
from .models import Collection
from vouchers.models import SaleVoucher
from django.contrib.auth.decorators import login_required
from challan.models import *
from .forms import CollectionFormSale, CollectionFormLocalSale
from core.views import sale_total_amount


def load_sale_vouchers(request):
    name = request.GET.get('name')
    challan = Challan.objects.filter(buyer_name=name)
    v_id = []
    for challan in challan:
        sale = SaleVoucher.objects.get(challan_no_id=challan.id)
        v_id.append(sale.voucher_number)
    vouchers = SaleVoucher.objects.filter(voucher_number__in=v_id).order_by('voucher_number')
    context = {
        'vouchers': vouchers,
    }
    return render(request, 'collections/voucher_dropdown_list_options.html', context)


def load_local_sale_vouchers(request):
    name = request.GET.get('name')
    vouchers = LocalSale.objects.filter(buyer_name=name).order_by('sale_no')
    context = {
        'vouchers': vouchers,
    }
    return render(request, 'collections/voucher_dropdown_list_options.html', context)


class CollectionCreateSale(LoginRequiredMixin, CreateView):
    form_class = CollectionFormSale
    template_name = 'collections/collection_add_form.html'

    def form_valid(self, form):
        form.instance.collected_by = self.request.user
        form.instance.sale_type = 'SALE'
        super().form_valid(form=form)
        voucher = get_object_or_404(Collection, collection_no=form.cleaned_data['collection_no'])
        data = {
            'general_voucher': None,
            'payment_no': None,
            'collection_no': voucher,
            'investment_no': None,
            'bk_payment_no': None,
            'description': 'From Sale',
            'type': 'C'
        }
        create_account_ledger(data)
        return HttpResponseRedirect(self.get_success_url())


class CollectionCreateLocalSale(LoginRequiredMixin, CreateView):
    form_class = CollectionFormLocalSale
    template_name = 'collections/collection_add_form.html'

    def form_valid(self, form):
        form.instance.collected_by = self.request.user
        form.instance.sale_type = 'LOCAL SALE'
        super().form_valid(form=form)
        voucher = get_object_or_404(Collection, collection_no=form.cleaned_data['collection_no'])
        data = {
            'general_voucher': None,
            'payment_no': None,
            'collection_no': voucher,
            'investment_no': None,
            'bk_payment_no': None,
            'description': 'From Sale',
            'type': 'C'
        }
        create_account_ledger(data)
        return HttpResponseRedirect(self.get_success_url())


class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'
    paginate_by = 20


class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = 'collections/collection_confirm_delete.html'
    success_url = '/collection_list'


class CollectionUpdateViewSale(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionFormSale
    template_name = 'collections/collection_update_form.html'


class CollectionUpdateViewLocalSale(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionFormLocalSale
    template_name = 'collections/collection_update_form.html'


@login_required()
def collection_details(request, pk):
    collection = Collection.objects.get(id=pk)
    collected_amount_word = string.capwords(num2words(collection.collection_amount))
    context = {
        'collection': collection,
        'collected_amount_word': collected_amount_word,
    }
    return render(request, 'collections/collection_detail.html', context)


@login_required()
def collection_report(request):
    sale_vouchers = SaleVoucher.objects.all()
    collections = Collection.objects.all()
    voucher_contains_query = request.GET.get('voucher_no')
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0
    total_collected = 0
    total_receivable = 0
    collection_due = 0
    collection = []

    if voucher_contains_query != '' and voucher_contains_query != 'Choose...':
        sale_voucher = sale_vouchers.filter(voucher_number=voucher_contains_query)

        for voucher in sale_voucher:
            collection = collections.filter(sale_voucher_no_id=voucher.id)
            total_collected = collections.filter(sale_voucher_no_id=voucher.id).aggregate(Sum('collection_amount'))
            rate = voucher.rate
            challan = Challan.objects.filter(challan_no=voucher.challan_no)

            for challan in challan:
                pass

            total_weight = challan.number_of_bag * challan.weight_per_bag
            total_amount = rate*total_weight

            if voucher.weight_of_each_bag is not None:
                total_self_weight_of_bag = voucher.weight_of_each_bag * challan.number_of_bag

            if voucher.per_bag_unloading_cost is not None:
                total_unloading_cost = voucher.per_bag_unloading_cost * challan.number_of_bag

            if voucher.measuring_cost_per_kg is not None:
                total_measuring_cost = voucher.measuring_cost_per_kg * total_weight

            weight_after_deduction = total_weight - total_self_weight_of_bag
            total_amount = rate*weight_after_deduction
            total_receivable = total_amount - total_unloading_cost - total_measuring_cost

        if total_collected != 0 and total_collected['collection_amount__sum'] is not None:
            print(total_collected['collection_amount__sum'])
            collection_due = total_receivable-total_collected['collection_amount__sum']

    context = {
        'page_obj': collection,
        'vouchers': sale_vouchers,
        'total_collected': total_collected,
        'total_receivable': total_receivable,
        'collection_due': collection_due,
        'sale_voucher': voucher_contains_query
    }
    return render(request, "collections/collection_report.html", context)


@login_required()
def collection_search(request):
    sale_vouchers = SaleVoucher.objects.all()
    sales = sale_vouchers
    collections = Collection.objects.all()
    persons = Persons.objects.all()
    challans = Challan.objects.all()
    name_contains_query = request.GET.get('name_contains')
    phone_query = request.GET.get('phone_contains')
    voucher_contains_query = request.GET.get('voucher_no')
    total_receivable = 0

    # filter collection by name
    if name_contains_query != '' and name_contains_query is not None:
        persons = persons.filter(person_name__contains=name_contains_query)
        v_id = []
        c_id = []
        for person in persons:
            challans = challans.filter(buyer_name=person.id)
        for challan in challans:
            c_id.append(challan.id)
        sales = sale_vouchers.filter(challan_no_id__in=c_id)
        for sale in sales:
            v_id.append(sale.id)
        collections = collections.filter(sale_voucher_no_id__in=v_id)

    # filter collection by sale voucher
    elif voucher_contains_query != '' and voucher_contains_query != 'Select Voucher No':
        sales = sale_vouchers.filter(voucher_number=voucher_contains_query)
        for sale in sales:
            collections = collections.filter(sale_voucher_no_id=sale.id)

    total_collected = collections.aggregate(Sum('collection_amount'))
    total_collected = total_collected['collection_amount__sum']

    for sale in sales:
        total_receivable = total_receivable + sale_total_amount(sale.id)

    print(total_receivable)

    context = {
        'collections': collections,
        'vouchers': sale_vouchers,
        'total_collected': total_collected,
        'total_receivable': total_receivable
    }
    return render(request, "collections/collection_search_form.html", context)