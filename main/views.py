from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from local_sale.models import LocalSale
from orders.models import Orders
from organizations.models import Persons
from payments.models import Payment
from payroll.models import Employee
from vouchers.models import SaleVoucher, BuyVoucher
from stocks.models import Stocks


# Create your views here.
@login_required()
def home(request):
    order_count = Orders.objects.all().count()
    persons = Persons.objects.all().count()
    sale_count = SaleVoucher.objects.all().count() + LocalSale.objects.all().count()
    buy_count = BuyVoucher.objects.all().count()
    payment_count = Payment.objects.all().count()
    employee_count = Employee.objects.all().count()
    context = {
        'payment_count': payment_count,
        'order_count': order_count,
        'sale_count': sale_count,
        'buy_count': buy_count,
        'employee_count': employee_count,
        'persons': persons,
        'tittle': 'techAlong Business | Home'
    }
    return render(request, 'main/home.html', context)


@login_required()
def settings(request):
    return render(request, 'main/settings_home.html')

