from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.digit2words import d2w
from ledger.views import create_account_ledger
from .forms import *
from challan.models import Challan
from organizations.models import Persons


# person creation from buy form
class PersonCreateBuy(LoginRequiredMixin, CreateView):
    model = Persons
    fields = '__all__'
    template_name = 'organizations/person_add.html'
    success_url = '/add_buy_voucher'


# buy voucher start
class BuyVoucherCreateView(LoginRequiredMixin, CreateView):
    form_class = BuyForm
    template_name = 'vouchers/buyvoucher_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'New Buy'
        context['button_name'] = 'Save'
        context['tittle'] = 'New Buy'
        return context


class BuyListView(LoginRequiredMixin, ListView):
    model = BuyVoucher
    template_name = 'vouchers/buy_list.html'
    context_object_name = 'vouchers'
    ordering = '-voucher_number'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voucher_selection = BuyVoucher.objects.all()
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
        context['tittle'] = 'Buy Voucher List'
        context['today'] = today
        return context

    def get_queryset(self):
        vouchers = BuyVoucher.objects.all().order_by('-date_added')
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
            vouchers = vouchers.filter(seller_name=person.id)

        # checking phone no from input
        if phone_no_contains != 'Select Phone No' and phone_no_contains != 'None':
            person = Persons.objects.get(contact_number=phone_no_contains)
            vouchers = vouchers.filter(seller_name=person.id)

        # checking voucher number from input
        if voucher_contains != '' and voucher_contains != 'Select Voucher':
            vouchers = vouchers.filter(voucher_number=voucher_contains)

        return vouchers


class BuyVoucherUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BuyForm
    model = BuyVoucher
    template_name = 'vouchers/buyvoucher_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Buy Update'
        context['button_name'] = 'Update'
        context['tittle'] = 'Buy Update'
        return context


class BuyDeleteView(LoginRequiredMixin, DeleteView):
    model = BuyVoucher
    template_name = 'main/confirm_delete.html'
    success_url = '/buy_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Buy Voucher'
        context['tittle'] = 'Buy Voucher Delete'
        context['cancel_url'] = '/buy_list'
        return context
# buy voucher end


# sale voucher start
class SaleCreateView(LoginRequiredMixin, CreateView):
    form_class = SaleForm
    template_name = 'vouchers/salevoucher_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'New Sale'
        context['button_name'] = 'Save'
        context['tittle'] = 'New Sale'
        return context


class SaleListView(LoginRequiredMixin, ListView):
    model = SaleVoucher
    template_name = 'vouchers/sale_list.html'
    context_object_name = 'vouchers'
    ordering = '-voucher_number'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voucher_selection = SaleVoucher.objects.all()
        challan_selection = Challan.objects.all()
        names = Persons.objects.all()

        challan_contains = self.request.GET.get('challan_no')
        if challan_contains is None:
            challan_contains = 'Select Challan'

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
        context['challan_selection'] = challan_selection
        context['challan_selected'] = challan_contains
        context['name_selected'] = name_contains
        context['phone_no_selected'] = phone_no_contains
        context['tittle'] = 'Sale List'
        context['today'] = today
        return context

    def get_queryset(self):
        vouchers = SaleVoucher.objects.all().order_by('-date_added')
        order = self.request.GET.get('orderby')
        challan_contains = self.request.GET.get('challan_no')
        if challan_contains is None:
            challan_contains = 'Select Challan'
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
            challan = Challan.objects.filter(buyer_name=person.id)
            vouchers = vouchers.filter(challan_no__in=challan)

        # checking phone no from input
        if phone_no_contains != 'Select Phone No' and phone_no_contains != 'None':
            person = Persons.objects.get(contact_number=phone_no_contains)
            challan = Challan.objects.filter(buyer_name=person.id)
            vouchers = vouchers.filter(challan_no__in=challan)

        # checking voucher number from input
        if voucher_contains != '' and voucher_contains != 'Select Voucher':
            vouchers = vouchers.filter(voucher_number=voucher_contains)

        # checking challan number from input
        if challan_contains != '' and challan_contains != 'Select Challan':
            challan = Challan.objects.get(challan_no=challan_contains)
            vouchers = vouchers.filter(challan_no=challan)

        return vouchers


class SaleUpdateView(LoginRequiredMixin, UpdateView):
    model = SaleVoucher
    form_class = SaleForm
    template_name = 'vouchers/salevoucher_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Sale Update'
        context['button_name'] = 'Update'
        context['tittle'] = 'Sale Update'
        return context


class SaleDeleteView(LoginRequiredMixin, DeleteView):
    model = SaleVoucher
    template_name = 'main/confirm_delete.html'
    success_url = '/sale_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Sale Voucher'
        context['tittle'] = 'Sale Voucher Delete'
        context['cancel_url'] = '/sale_list'
        return context
# sale voucher end


class GeneralVoucherCreateView(LoginRequiredMixin, CreateView):
    form_class = GeneralForm
    template_name = 'vouchers/general_voucher_form.html'

    def form_valid(self, form):
        form.save()
        voucher = get_object_or_404(GeneralVoucher, voucher_number=form.cleaned_data['voucher_number'])
        data = {
            'general_voucher': voucher,
            'payment_no': None,
            'collection_no': None,
            'investment_no': None,
            'bk_payment_no': None,
            'salary_payment': None,
            'description': voucher.cost_Descriptions,
            'type': 'G',
            'date': voucher.date_added
        }
        create_account_ledger(data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'New General Voucher'
        context['button_name'] = 'Save'
        context['tittle'] = 'New General Voucher'
        return context


class GeneralVoucherUpdateView(LoginRequiredMixin, UpdateView):
    model = GeneralVoucher
    form_class = GeneralForm
    template_name = 'vouchers/general_voucher_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update General Voucher'
        context['button_name'] = 'Update'
        context['tittle'] = 'Update General Voucher'
        return context


class GeneralVoucherListView(LoginRequiredMixin, ListView):
    model = GeneralVoucher
    template_name = 'vouchers/general_voucher_list.html'
    context_object_name = 'vouchers'
    ordering = '-voucher_number'


class GeneralVoucherDeleteView(LoginRequiredMixin, DeleteView):
    model = GeneralVoucher
    template_name = 'main/confirm_delete.html'
    success_url = '/general_voucher_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'General Voucher'
        context['tittle'] = 'General Voucher Delete'
        context['cancel_url'] = '/general_voucher_list'
        return context
# sale general voucher end


@login_required()
def sale_details(request, pk):
    sale = SaleVoucher.objects.get(id=pk)
    challan = Challan.objects.filter(challan_no=sale.challan_no)
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0
    moisture_weight = 0
    seed_weight = 0
    fotka_weight = 0
    fotka_amount = 0
    
    for challan in challan:
        pass

    challan_weight = challan.weight
    total_challan_amount = challan_weight*sale.rate

    total_self_weight_of_bag = challan.number_of_bag * sale.weight_of_each_bag

    if sale.fotka_weight is not None:
        fotka_weight = sale.fotka_weight
        fotka_amount = fotka_weight * sale.fotka_rate

    if sale.moisture_weight is not None:
        moisture_weight = sale.moisture_weight

    if sale.seed_weight is not None:
        seed_weight = sale.seed_weight

    weight_after_deduction = challan_weight - moisture_weight - seed_weight - fotka_weight - total_self_weight_of_bag
    amount_after_deduction = weight_after_deduction * sale.rate
    net_amount = amount_after_deduction + fotka_amount
    net_amount = round(net_amount, 2)
    net_amount_in_words = d2w(net_amount)
    context = {
        'sale': sale,
        'challan': challan,
        'total_weight': challan_weight,
        'weight_after_deduction': weight_after_deduction,
        'amount_after_deduction': amount_after_deduction,
        'total_challan_amount': total_challan_amount,
        'fotka_amount': fotka_amount,
        'total_self_weight_of_bag': total_self_weight_of_bag,
        'total_measuring_cost': total_measuring_cost,
        'net_amount': net_amount,
        'net_amount_in_words': net_amount_in_words
    }
    return render(request, 'vouchers/sale_detail.html', context)


@login_required()
def buy_details(request, pk):
    buy = BuyVoucher.objects.get(id=pk)
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0

    total_weight = buy.weight
    total_amount = total_weight*buy.rate

    if buy.weight_of_each_bag is not None:
        total_self_weight_of_bag = buy.weight_of_each_bag*buy.number_of_bag

    if buy.per_bag_unloading_cost is not None:
        total_unloading_cost = buy.per_bag_unloading_cost*buy.number_of_bag

    if buy.measuring_cost_per_kg is not None:
        total_measuring_cost = buy.measuring_cost_per_kg*total_weight

    weight_after_deduction = total_weight - total_self_weight_of_bag
    total_amount_without_bag = buy.rate * weight_after_deduction
    amount_after_deduction = total_amount_without_bag - total_unloading_cost - total_measuring_cost
    grand_total_amount = amount_after_deduction + buy.previous_amount
    net_amount_in_words = d2w(grand_total_amount)

    context = {
        'buy': buy,
        'grand_total_amount': grand_total_amount,
        'total_weight': total_weight,
        'weight_after_deduction': weight_after_deduction,
        'amount_after_deduction': amount_after_deduction,
        'total_amount': total_amount,
        'total_unloading_cost': total_unloading_cost,
        'total_self_weight_of_bag': total_self_weight_of_bag,
        'total_measuring_cost': total_measuring_cost,
        'net_amount_in_words': net_amount_in_words
    }
    return render(request, 'vouchers/buy_detail.html', context)