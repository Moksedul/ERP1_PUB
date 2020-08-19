from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import *
from challan.models import Challan
from organizations.models import Persons
from daily_cash.views import create_daily_cash


# person creation from buy form
class PersonCreateBuy(LoginRequiredMixin, CreateView):
    model = Persons
    fields = '__all__'
    template_name = 'vouchers/person_add.html'
    success_url = '/add_buy_voucher'


# buy voucher start
class BuyVoucherCreateView(LoginRequiredMixin, CreateView):
    form_class = BuyForm
    template_name = 'vouchers/buyvoucher_add_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class BuyListView(LoginRequiredMixin, ListView):
    model = BuyVoucher
    template_name = 'vouchers/buy_list.html'
    context_object_name = 'vouchers'
    paginate_by = 20


class BuyVoucherUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BuyForm
    model = BuyVoucher
    template_name = 'vouchers/buyvoucher_update_form.html'


class BuyDeleteView(LoginRequiredMixin, DeleteView):
    model = BuyVoucher
    success_url = '/buy_list'
# buy voucher end


# sale voucher start
class SaleCreateView(LoginRequiredMixin, CreateView):
    form_class = SaleForm
    template_name = 'vouchers/salevoucher_add_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class SaleListView(LoginRequiredMixin, ListView):
    model = SaleVoucher
    template_name = 'vouchers/sale_list.html'
    context_object_name = 'vouchers'
    paginate_by = 20


class SaleUpdateView(LoginRequiredMixin, UpdateView):
    model = SaleVoucher
    form_class = SaleForm
    template_name = 'vouchers/sale_update_form.html'


class SaleDeleteView(LoginRequiredMixin, DeleteView):
    model = SaleVoucher
    template_name = 'vouchers/sale_confirm_delete.html'
    success_url = '/sale_list'
# sale voucher end


# general voucher start
def general_voucher_create(request):
    context = {}
    form = GeneralForm(request.POST or None)

    if form.is_valid():
        form.save()
        voucher = get_object_or_404(GeneralVoucher, voucher_number=form.cleaned_data['voucher_number'])
        data = {
            'general_voucher': voucher,
            'payment_no': None,
            'collection_no': None,
            'investment_no': None,
            'description': voucher.cost_Descriptions,
            'type': 'G'
        }
        create_daily_cash(data)

    context['form'] = form
    return render(request, 'vouchers/general_voucher_add_form.html', context)


class GeneralVoucherCreateView(LoginRequiredMixin, CreateView):
    form_class = GeneralForm
    template_name = 'vouchers/general_voucher_add_form.html'

    def form_valid(self, form):
        form.save()
        voucher = get_object_or_404(GeneralVoucher, voucher_number=form.cleaned_data['voucher_number'])
        data = {
            'general_voucher': voucher,
            'payment_no': None,
            'collection_no': None,
            'investment_no': None,
            'description': voucher.cost_Descriptions,
            'type': 'G'
        }
        create_daily_cash(data)
        return super().form_valid(form)


class GeneralVoucherUpdateView(LoginRequiredMixin, UpdateView):
    model = GeneralVoucher
    template_name = 'vouchers/general_voucher_update_form.html'
    fields = '__all__'


class GeneralVoucherListView(LoginRequiredMixin, ListView):
    model = GeneralVoucher
    template_name = 'vouchers/general_voucher_list.html'
    context_object_name = 'vouchers'
    paginate_by = 20


class GeneralVoucherDeleteView(LoginRequiredMixin, DeleteView):
    model = GeneralVoucher
    template_name = 'vouchers/general_voucher_confirm_delete.html'
    success_url = '/general_voucher_list'
# sale general voucher end


@login_required()
def sale_details(request, pk):
    sale = SaleVoucher.objects.get(id=pk)
    challan = Challan.objects.filter(challan_no=sale.challan_no)
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0

    for challan in challan:
        pass

    total_weight = challan.weight
    total_amount = total_weight*sale.rate

    if sale.weight_of_each_bag is not None:
        total_self_weight_of_bag = sale.weight_of_each_bag*challan.number_of_bag

    if sale.per_bag_unloading_cost is not None:
        total_unloading_cost = sale.per_bag_unloading_cost*challan.number_of_bag

    if sale.measuring_cost_per_kg is not None:
        total_measuring_cost = sale.measuring_cost_per_kg*total_weight

    weight_after_deduction = total_weight - total_self_weight_of_bag
    total_amount_without_bag = sale.rate*weight_after_deduction
    amount_after_deduction = total_amount_without_bag - total_unloading_cost - total_measuring_cost

    context = {
        'sale': sale,
        'challan': challan,
        'total_weight': total_weight,
        'weight_after_deduction': weight_after_deduction,
        'amount_after_deduction': amount_after_deduction,
        'total_amount': total_amount,
        'total_unloading_cost': total_unloading_cost,
        'total_self_weight_of_bag': total_self_weight_of_bag,
        'total_measuring_cost': total_measuring_cost
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

    context = {
        'buy': buy,
        'grand_total_amount': grand_total_amount,
        'total_weight': total_weight,
        'weight_after_deduction': weight_after_deduction,
        'amount_after_deduction': amount_after_deduction,
        'total_amount': total_amount,
        'total_unloading_cost': total_unloading_cost,
        'total_self_weight_of_bag': total_self_weight_of_bag,
        'total_measuring_cost': total_measuring_cost
    }
    return render(request, 'vouchers/buy_detail.html', context)