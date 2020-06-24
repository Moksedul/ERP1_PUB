from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Sum
import string
from num2words import num2words
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Collection
from vouchers.models import SaleVoucher
from django.contrib.auth.decorators import login_required
from challan.models import Challan
from .forms import CollectionForm


class CollectionCreate(LoginRequiredMixin, CreateView):
    form_class = CollectionForm
    template_name = 'collections/collection_add_form.html'


class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'
    paginate_by = 5


class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = 'collections/collection_confirm_delete.html'
    success_url = '/collection_list'


class CollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collection_update_form.html'


@login_required()
def collection_details(request, pk):
    collection = Collection.objects.get(id=pk)
    collected_amount_word = string.capwords(num2words(collection.collection_amount))
    context = {
        'collection': collection,
        'collected_amount_word': collected_amount_word,
    }
    return render(request, 'collections/collection_Detail.html', context)


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

    if voucher_contains_query != '' and voucher_contains_query is not 'Choose...':
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
    sale_voucher = SaleVoucher.objects.all()
    collections = Collection.objects.all()
    name_contains_query = request.GET.get('name_contains')
    voucher_contains_query = request.GET.get('voucher_no')
    total = 0

    if name_contains_query != '' and name_contains_query is not None:
        sales = sale_voucher.filter(payed_to__contains=name_contains_query)
    elif voucher_contains_query != '' and voucher_contains_query is not 'Choose...':
        buy_voucher = sale_voucher.filter(voucher_number=voucher_contains_query)
        for voucher in buy_voucher:
            collections = collections.filter(sale_voucher_no_id=voucher.id)
            total = collections.filter(sale_voucher_no_id=voucher.id).aggregate(Sum('collection_amount'))
    paginator = Paginator(collections, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'vouchers': sale_voucher,
        'total': total
    }
    return render(request, "collections/collection_search_form.html", context)