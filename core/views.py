from django.contrib.auth.decorators import login_required
from challan.models import Challan
from vouchers.models import *


def sale_details(pk):
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


def buy_details(pk):
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
    print(weight_after_deduction)
    context = {
        'buy': buy,
        'total_weight': total_weight,
        'weight_after_deduction': weight_after_deduction,
        'amount_after_deduction': amount_after_deduction,
        'total_amount': total_amount,
        'total_unloading_cost': total_unloading_cost,
        'total_self_weight_of_bag': total_self_weight_of_bag,
        'total_measuring_cost': total_measuring_cost
    }