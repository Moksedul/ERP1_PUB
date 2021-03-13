from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
import string
from num2words import num2words
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ledger.views import create_account_ledger, update_account_ledger
from local_sale.models import LocalSale
from .filters import CollectionFilter
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
    template_name = 'collections/collection_form.html'

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
            'salary_payment': None,
            'date': voucher.collection_date,
            'description': 'From Sale',
            'type': 'C'
        }
        create_account_ledger(data)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        super().form_valid(form=form)
        voucher = get_object_or_404(Collection, collection_no=form.cleaned_data['collection_no'])
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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        names = Persons.objects.all()
        sale_vouchers_selection = SaleVoucher.objects.all()
        local_sale_voucher_selection = LocalSale.objects.all()
        voucher_contains = self.request.GET.get('voucher_no')
        if voucher_contains is None:
            voucher_contains = 'Select Voucher'
        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'
        phone_no_contains = self.request.GET.get('phone_no')
        print(phone_no_contains)
        if phone_no_contains is None or phone_no_contains == '':
            phone_no_contains = 'Select Phone No'
            print(phone_no_contains)

        voucher_list = {'voucher': []}
        for sale in sale_vouchers_selection:
            key = "voucher"
            voucher_list.setdefault(key, [])
            voucher_list[key].append({'voucher_no': sale.voucher_number})
        for local_sale in local_sale_voucher_selection:
            key = "voucher"
            voucher_list.setdefault(key, [])
            voucher_list[key].append({'voucher_no': local_sale.sale_no})

        context['names'] = names
        context['sale_voucher_selection'] = voucher_list['voucher']
        context['voucher_selected'] = voucher_contains
        context['name_selected'] = name_contains
        context['phone_no_selected'] = phone_no_contains
        context['form_name'] = 'Update Sale Collection'
        context['button_name'] = 'Update'
        context['tittle'] = 'Collection List'
        return context

    def get_queryset(self):
        sale_vouchers = SaleVoucher.objects.all()
        local_sale_vouchers = LocalSale.objects.all()
        collections = Collection.objects.all()
        order = self.request.GET.get('orderby')
        voucher_contains = self.request.GET.get('voucher_no')
        # name_contains = self.request.GET.get('name')
        # phone_no_contains = self.request.GET.get('phone_no')
        if voucher_contains is None:
            voucher_contains = 'Select Voucher'
        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'
        phone_no_contains = self.request.GET.get('phone_no')
        print(phone_no_contains)
        if phone_no_contains is None or phone_no_contains == '':
            phone_no_contains = 'Select Phone No'
            print(phone_no_contains)
        collection_all = Collection.objects.all().order_by('-collection_date')
        collection_final = collection_all

        # checking name from input
        if name_contains != 'Select Name':
            person = Persons.objects.get(person_name=name_contains)
            challans = Challan.objects.filter(buyer_name=person.id)
            v_id = []
            for challan in challans:
                v_id.append(challan.id)
            sale_vouchers = sale_vouchers.filter(challan_no__in=v_id)
            local_sale_vouchers = local_sale_vouchers.filter(buyer_name=person.id)
            collections = collections.filter(collected_from=person.id)

        # checking phone no from input
        if phone_no_contains != 'Select Phone No':
            print(phone_no_contains)
            person = Persons.objects.get(contact_number=phone_no_contains)
            challans = Challan.objects.filter(buyer_name=person.id)
            v_id = []
            for challan in challans:
                v_id.append(challan.id)
            sale_vouchers = sale_vouchers.filter(challan_no__in=v_id)
            local_sale_vouchers = local_sale_vouchers.filter(buyer_name=person.id)
            collections = collections.filter(collected_from=person.id)

        # checking voucher number from input
        if voucher_contains != '' and voucher_contains != 'Select Voucher':
            sale_vouchers = sale_vouchers.filter(voucher_number=voucher_contains)
            if sale_vouchers:
                local_sale_vouchers = LocalSale.objects.none()
                v_id = []
                for voucher in sale_vouchers:
                    v_id.append(voucher.id)
                collections = collections.filter(sale_voucher_no_id__in=v_id)
            else:
                sale_vouchers = SaleVoucher.objects.none()
                local_sale_vouchers = local_sale_vouchers.filter(sale_no=voucher_contains)
                v_id = []
                for voucher in local_sale_vouchers:
                    v_id.append(voucher.id)
                collections = collections.filter(local_sale_voucher_no_id__in=v_id)
        collection_final = collections
        return collection_final


def collection_list(request):
    context = {}
    filtered_collections = CollectionFilter(
        request.GET,
        queryset=Collection.objects.all()
    )
    context['filtered_collections'] = filtered_collections
    paginated_collections = Paginator(filtered_collections.qs, 2)
    page_number = request.GET.get('page')
    page_obj = paginated_collections.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, 'collections/collection_list_filtered.html', context=context)


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
        super().form_valid(form=form)
        voucher = get_object_or_404(Collection, collection_no=form.cleaned_data['collection_no'])

        data = {
            'date': voucher.collection_date
        }
        update_account_ledger(data, voucher.pk)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        super().form_valid(form=form)
        voucher = get_object_or_404(Collection, collection_no=form.cleaned_data['collection_no'])

        data = {
            'date': voucher.collection_date
        }
        update_account_ledger(data, voucher.pk)
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
    collected_amount_word = string.capwords(num2words(collection.collection_amount))
    context = {
        'collection': collection,
        'collected_amount_word': collected_amount_word,
    }
    return render(request, 'collections/collection_detail.html', context)


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