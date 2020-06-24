from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from orders.models import Orders
from vouchers.models import SaleVoucher, BuyVoucher
from stocks.models import Stocks


# Create your views here.
@login_required()
def home(request):
    orders = Orders.objects.all()
    stocks = Stocks.objects.all()
    order_count = orders.count()
    sale_count = SaleVoucher.objects.all().count()
    buy_count = BuyVoucher.objects.all().count()

    # limiting stocks items to show
    paginator = Paginator(stocks, 3)
    page_number = request.GET.get('page')
    stocks = paginator.get_page(page_number)

    # limiting order items to show
    paginator = Paginator(orders, 3)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {
        'order_count': order_count,
        'sale_count': sale_count,
        'buy_count': buy_count,
        'orders': orders,
        'stocks': stocks
    }
    return render(request, 'main/home.html', context)


@login_required()
def settings(request):
    return render(request, 'main/settings_home.html')

