from vouchers.models import *


def sale_total_amount(pk):
    sale = SaleVoucher.objects.get(id=pk)
    challan = Challan.objects.filter(challan_no=sale.challan_no)
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0

    for challan in challan:
        pass

    total_weight = challan.weight

    if sale.weight_of_each_bag is not None:
        total_self_weight_of_bag = sale.weight_of_each_bag*challan.number_of_bag

    if sale.per_bag_unloading_cost is not None:
        total_unloading_cost = sale.per_bag_unloading_cost*challan.number_of_bag

    if sale.measuring_cost_per_kg is not None:
        total_measuring_cost = sale.measuring_cost_per_kg*total_weight

    weight_after_deduction = total_weight - total_self_weight_of_bag
    total_amount_without_bag = sale.rate*weight_after_deduction
    amount_after_deduction = total_amount_without_bag - total_unloading_cost - total_measuring_cost
    return amount_after_deduction


def buy_total_amount(pk):
    buy = BuyVoucher.objects.get(id=pk)
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0

    total_weight = buy.weight

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
    return grand_total_amount


def serial_no(initial, model_name):
    last_serial = model_name.objects.all().order_by('id').last()
    if not last_serial:
        return initial + '0001'
    serial_number = last_serial.voucher_number
    serial_int = int(serial_number.split(initial)[-1])
    new_serial_int = serial_int + 1
    new_serial_no = ''
    if new_serial_int < 10:
        new_serial_no = initial + '000' + str(new_serial_int)
    if 100 > new_serial_int >= 10:
        new_serial_no = initial + '00' + str(new_serial_int)
    if 100 <= new_serial_int < 1000:
        new_serial_no = initial + '0' + str(new_serial_int)
    if new_serial_int >= 1000:
        new_serial_no = initial + str(new_serial_int)
    return new_serial_no