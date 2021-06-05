from datetime import datetime

from django.shortcuts import render

from LC.models import LC, LCProduct, LCExpense
from accounts.models import Investment
from bkash.models import PaymentBkashAgent
from collection.models import Collection
from ledger.models import AccountLedger
from local_sale.models import LocalSale, Product
from payments.models import Payment
from payroll.models import SalaryPayment
from vouchers.models import SaleVoucher, Persons, GeneralVoucher, BuyVoucher


def load_person_image(request):
    name = request.GET.get('name')
    person = Persons.objects.get(id=name)
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


def sale_total_amount(pk):
    sale = SaleVoucher.objects.get(id=pk)
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0
    moisture_weight = 0
    weight_for_moisture_percentage = 0
    seed_weight = 0
    fotka_weight = 0
    fotka_amount = 0

    challan_weight = sale.challan_no.total_weight
    total_self_weight_of_bag = sale.challan_no.number_of_bag * sale.weight_of_each_bag

    if sale.spot_weight is not None and sale.spot_rate is not None:
        spot_weight = sale.spot_weight
        fotka_amount = spot_weight * sale.spot_rate

    if sale.moisture_weight is not None:
        moisture_weight = sale.moisture_weight

    if sale.moisture_percentage is not None:
        weight_for_moisture_percentage = (sale.moisture_percentage/100) * challan_weight
        moisture_weight = moisture_weight + weight_for_moisture_percentage

    if sale.seed_weight is not None:
        seed_weight = sale.seed_weight

    weight_after_deduction = challan_weight - moisture_weight - seed_weight - fotka_weight - total_self_weight_of_bag
    amount_after_deduction = weight_after_deduction * sale.rate
    net_amount = amount_after_deduction + fotka_amount
    net_amount = round(net_amount, 2)
    return net_amount


def local_sale_total_amount(pk):
    sale = LocalSale.objects.get(id=pk)
    products = Product.objects.filter(sale_no_id=sale.id)
    product_total = 0

    for product in products:
        amount = product.rate * product.weight
        product_total += amount

    if sale.transport_charge_payee == 'CUSTOMER':
        voucher_total = product_total + sale.transport_charge
    else:
        voucher_total = product_total - sale.transport_charge

    grand_total_amount = voucher_total + sale.previous_due - sale.discount

    return grand_total_amount


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

    rate = 0
    if buy.rate_per_kg is not None and buy.rate_per_kg !=0:
        rate = buy.rate_per_kg
    elif buy.rate_per_mann is not None and buy.rate_per_mann !=0:
        rate = buy.rate_per_mann/40.0
    else:
        rate = rate

    weight_after_deduction = total_weight - total_self_weight_of_bag
    total_amount_without_bag = rate * weight_after_deduction
    amount_after_deduction = total_amount_without_bag - total_unloading_cost - total_measuring_cost
    if not buy.previous_amount:
        buy.previous_amount = 0
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