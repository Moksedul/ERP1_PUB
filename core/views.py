from datetime import datetime

from django.shortcuts import render

from LC.models import LC, LCProduct, LCExpense
from accounts.models import Investment
from bkash.models import PaymentBkashAgent
from collection.models import Collection
from core.digit2words import d2w
from ledger.models import AccountLedger
from local_sale.models import LocalSale, Product
from payments.models import Payment
from payroll.models import SalaryPayment
from vouchers.models import SaleVoucher as Sale, Persons, GeneralVoucher, BuyVoucher, SaleExpense


def load_person_image(request):
    name = request.GET.get('name')

    try:
        person = Persons.objects.get(id=name)
    except:
        person = []
    context = {
        'person': person,
    }
    return render(request, 'main/person_image.html', context)


def lc_total_amount(pk):
    lc = LC.objects.get(id=pk)
    products = LCProduct.objects.filter(lc=lc.id)
    expenses = LCExpense.objects.filter(lc=lc.id)
    product_total = 0
    expense_total = 0

    for product in products:
        product_total += product.rate * product.weight

    for expense in expenses:
        expense_total += expense.amount

    lc_total = product_total + expense_total

    return lc_total


def sale_detail_calc(pk):
    sale = Sale.objects.get(id=pk)
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0
    moisture_weight = 0
    seed_weight = 0
    spot_weight = 0
    spot_amount = 0
    seed_amount = 0

    challan_weight = sale.challan_no.total_weight
    total_challan_amount = challan_weight * sale.rate

    total_self_weight_of_bag = sale.challan_no.number_of_bag * sale.weight_of_each_bag

    if sale.spot_weight is not None:
        spot_weight = sale.spot_weight + ((sale.spot_percentage / 100) * challan_weight)
        spot_amount = spot_weight * sale.spot_rate

    if sale.moisture_weight is not None:
        moisture_weight = sale.moisture_weight + ((sale.moisture_percentage / 100) * challan_weight)

    if sale.seed_weight is not None:
        seed_weight = sale.seed_weight + ((sale.seed_percentage / 100) * challan_weight)
        seed_amount = seed_weight * sale.seed_rate

    weight_after_deduction = challan_weight - moisture_weight - total_self_weight_of_bag - seed_weight - spot_weight + sale.weight_adjusted
    weight_with_spot_and_seed = weight_after_deduction + spot_weight + seed_weight
    amount_after_deduction = weight_after_deduction * sale.rate
    if sale.weight_percentage_TDS > 0 and sale.amount_percentage_TDS > 0:
        tds_weight_ratio = sale.weight_percentage_TDS/100
        tds_percentage_amount = sale.amount_percentage_TDS/100
        amount_tds = amount_after_deduction*tds_weight_ratio*tds_percentage_amount
    else:
        amount_tds = 0
    net_amount = amount_after_deduction + spot_amount + seed_amount + amount_tds
    net_amount = round(net_amount, 2)
    net_amount_in_words = d2w(net_amount)

    # profit analysis
    sale_expanses = SaleExpense.objects.filter(sale=sale)
    total_expanse = 0
    for expanse in sale_expanses:
        total_expanse += expanse.amount

    total_unloading_cost = sale.challan_no.number_of_bag * sale.per_bag_unloading_cost
    total_measuring_cost = challan_weight * sale.measuring_cost_per_kg
    total_expanse += total_measuring_cost + total_unloading_cost
    actual_revenue_receivable = net_amount - total_expanse
    if challan_weight !=0:
        actual_rate_receivable = actual_revenue_receivable / challan_weight
    else:
        actual_rate_receivable = 0

    context = {

        'sale': sale,
        'sale_expanses': sale_expanses,
        'total_expanse': round(total_expanse, 2),
        'total_weight': challan_weight,
        'actual_revenue_receivable': round(actual_revenue_receivable, 2),
        'actual_rate_receivable': round(actual_rate_receivable, 2),
        'weight_after_deduction': round(weight_after_deduction, 2),
        'weight_with_spot_and_seed': round(weight_with_spot_and_seed, 2),
        'amount_after_deduction': round(amount_after_deduction, 2),
        'total_challan_amount': round(total_challan_amount, 2),
        'spot_weight': round(spot_weight, 2),
        'moisture_weight': round(moisture_weight, 2),
        'seed_weight': round(seed_weight, 2),
        'seed_amount': round(seed_amount, 2),
        'fotka_amount': round(spot_amount, 2),
        'total_self_weight_of_bag': total_self_weight_of_bag,
        'total_measuring_cost': round(total_measuring_cost, 2),
        'total_unloading_cost': round(total_unloading_cost, 2),
        'net_amount': net_amount,
        'net_amount_in_words': net_amount_in_words
    }
    return context


def local_sale_detail_calc(pk):
    sale = LocalSale.objects.get(id=pk)
    products = Product.objects.filter(sale_no_id=sale.id)
    product_total = 0

    product_list = {
        'products': []

    }

    for product in products:
        amount = product.rate * product.weight
        product_total += amount
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

    return context


def buy_details_calc(pk):
    buy = BuyVoucher.objects.get(id=pk)
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0
    previous_amount = 0

    rate = 0
    if buy.rate_per_kg is not None and buy.rate_per_kg != 0:
        rate = buy.rate_per_kg
    elif buy.rate_per_mann is not None and buy.rate_per_mann != 0:
        rate = buy.rate_per_mann / 40.0
    else:
        rate = rate

    total_weight = buy.weight
    total_amount = total_weight * rate

    if buy.weight_of_each_bag is not None:
        total_self_weight_of_bag = buy.weight_of_each_bag * buy.number_of_bag

    if buy.per_bag_unloading_cost is not None:
        total_unloading_cost = buy.per_bag_unloading_cost * buy.number_of_bag

    if buy.measuring_cost_per_kg is not None:
        total_measuring_cost = buy.measuring_cost_per_kg * total_weight

    if buy.previous_amount:
        previous_amount = buy.previous_amount

    if buy.transport_cost_payee == 'Buyer':
        transport_cost = buy.transport_cost
    else:
        transport_cost = -buy.transport_cost

    weight_after_deduction = total_weight - total_self_weight_of_bag
    total_amount_without_bag = rate * weight_after_deduction
    amount_after_deduction = total_amount_without_bag - total_unloading_cost - total_measuring_cost
    grand_total_amount = amount_after_deduction + previous_amount - buy.discount + transport_cost
    net_amount_in_words = d2w(round(grand_total_amount, 2))

    context = {
        'buy': buy,
        'grand_total_amount': round(grand_total_amount, 2),
        'total_weight': round(total_weight, 2),
        'weight_after_deduction': round(weight_after_deduction, 2),
        'amount_after_deduction': round(amount_after_deduction, 2),
        'total_amount': round(total_amount, 2),
        'total_unloading_cost': total_unloading_cost,
        'total_self_weight_of_bag': total_self_weight_of_bag,
        'total_measuring_cost': total_measuring_cost,
        'net_amount_in_words': net_amount_in_words,
        'transport_cost': transport_cost,
    }

    return context


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


def account_balance_calc(pk):
    selected_account = pk
    account_ledgers = AccountLedger.objects.all()
    account_balance = 0

    ledgers = {
        'voucher': []

    }

    for account_ledger in account_ledgers:
        # for agent payment
        if account_ledger.type == 'BK':
            bkash_payment = PaymentBkashAgent.objects.filter(payment_from_account_id=selected_account)
            bkash_payment = bkash_payment.filter(id=account_ledger.bk_payment_no_id)
            for bkash_payment in bkash_payment:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'debit_amount': bkash_payment.amount,
                    'credit_amount': 0,
                })
        # for general payment
        if account_ledger.type == 'G':
            general_voucher = GeneralVoucher.objects.filter(from_account_id=selected_account)
            general_voucher = general_voucher.filter(id=account_ledger.general_voucher_id)
            for general_voucher in general_voucher:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'debit_amount': general_voucher.cost_amount,
                    'credit_amount': 0,
                })

        # for SalaryP payment
        if account_ledger.type == 'SP':
            salary_payment = SalaryPayment.objects.filter(payment_from_account_id=selected_account)
            salary_payment = salary_payment.filter(id=account_ledger.salary_payment_id)
            for salary_payment in salary_payment:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'debit_amount': salary_payment.amount,
                    'credit_amount': 0,
                })

        # for buy payment
        if account_ledger.type == 'P':
            payment = Payment.objects.filter(payment_from_account_id=selected_account)
            payment = payment.filter(pk=account_ledger.payment_no_id)
            for payment in payment:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'debit_amount': payment.payment_amount,
                    'credit_amount': 0,
                })

        # for investment
        if account_ledger.type == 'I':
            investment_credit = Investment.objects.filter(investing_to_account_id=selected_account)
            investment_credit = investment_credit.filter(pk=account_ledger.investment_no_id)
            investment_debit = Investment.objects.filter(investing_from_account_id=selected_account)
            investment_debit = investment_debit.filter(pk=account_ledger.investment_no_id)

            for investment in investment_credit:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'debit_amount': 0,
                    'credit_amount': investment.investing_amount,
                })
            for investment_debit in investment_debit:
                key = "voucher"
                ledgers.setdefault(key, [])
                ledgers[key].append({
                    'debit_amount': investment_debit.investing_amount,
                    'credit_amount': 0,
                })

        # for Collection
        if account_ledger.type == 'C':
            collection = Collection.objects.filter(collection_to_account_id=selected_account)
            collection = collection.filter(pk=account_ledger.collection_no_id)

            for collection in collection:
                if collection.sale_type == 'SALE':
                    if collection.sale_voucher_no_id is not None:
                        key = "voucher"
                        ledgers.setdefault(key, [])
                        ledgers[key].append({
                            'debit_amount': 0,
                            'credit_amount': collection.collection_amount,
                        })
                    else:
                        key = "voucher"
                        ledgers.setdefault(key, [])
                        ledgers[key].append({
                            'debit_amount': 0,
                            'credit_amount': collection.collection_amount,
                        })

                else:
                    if collection.local_sale_voucher_no is not None:
                        key = "voucher"
                        ledgers.setdefault(key, [])
                        ledgers[key].append({
                            'debit_amount': 0,
                            'credit_amount': collection.collection_amount,
                        })
                    else:
                        key = "voucher"
                        ledgers.setdefault(key, [])
                        ledgers[key].append({
                            'debit_amount': 0,
                            'credit_amount': collection.collection_amount,
                        })

    for item in ledgers['voucher']:
        account_balance = account_balance - item['debit_amount'] + item['credit_amount']

    return account_balance


def time_difference(time_1, time2):
    time_1 = datetime.strptime(str(time_1), '%H:%M:%S')
    time_2 = datetime.strptime(str(time2), '%H:%M:%S')
    difference = (time_2 - time_1)
    pt = datetime.strptime(str(difference), '%H:%M:%S')
    total_seconds = pt.second + pt.minute * 60 + pt.hour * 3600
    return total_seconds