from django.shortcuts import render
from django.db.models import Sum
from django.core.paginator import Paginator
import string
from num2words import num2words
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Collection
from vouchers.models import SaleVoucher
from django.contrib.auth.decorators import login_required
from accounts.models import Accounts
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
    total = 0

    if voucher_contains_query != '' and voucher_contains_query is not 'Choose...':
        sale_vouchers = sale_vouchers.filter(sale_voucher_no=voucher_contains_query)
        for voucher in sale_vouchers:
            collection = collections.filter(voucher_no_id=voucher.id)
            total = collections.filter(voucher_no_id=voucher.id).aggregate(Sum('collection_amount'))
    paginator = Paginator(collections, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'vouchers': sale_vouchers,
        'total': total
    }
    return render(request, "collections/collection_report.html", context)