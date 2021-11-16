from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from organizations.models import Organization
from products.models import Products
from vouchers.models import BuyVoucher
from .forms import StockForm, StockUpdateForm
from .models import Stock, Store


# Create your views here.
class StockCreateView(LoginRequiredMixin, CreateView):
    form_class = StockForm
    template_name = 'stocks/stock_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Save'
        context['tittle'] = 'Add Stock'
        return context


def stock_view(request):
    stocks = Stock.objects.all()
    all_weights = []
    for stock in stocks:
        all_weights.append(stock.weight)
    total_weight = sum(all_weights)
    context = {"total_weight": int(total_weight)}
    return render(request, 'stocks/report.html', context)


class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'stocks/stock_list.html'
    context_object_name = 'stocks'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Products.objects.all()
        business_names = Organization.objects.all()
        stores = Store.objects.all()

        product_contains = self.request.GET.get('product')
        if product_contains is None:
            product_contains = 'Select Product'
        business_contains = self.request.GET.get('business')
        if business_contains is None or business_contains == '':
            business_contains = 'Select Business'
        store_contains = self.request.GET.get('store')
        if store_contains is None or store_contains == '':
            store_contains = 'Select store'

        context['products'] = products
        context['product_selected'] = product_contains
        context['stores'] = stores
        context['store_selected'] = store_contains
        context['business_selected'] = business_contains
        context['business_names'] = business_names
        context['tittle'] = 'Stock List'
        return context

    def get_queryset(self):
        stocks = Stock.objects.all().order_by('-last_updated_time')
        product_contains = self.request.GET.get('product')
        business_contains = self.request.GET.get('business')
        store_contains = self.request.GET.get('store')

        if product_contains != 'Select Product' and product_contains is not None:
            product = Products.objects.get(product_name=product_contains)
            stocks = stocks.filter(product=product)

        if business_contains != 'Select Business' and business_contains is not None:
            business = Organization.objects.get(name=business_contains)
            stocks = stocks.filter(business_name=business)

        if store_contains != 'Select store' and business_contains is not None:
            store = Store.objects.get(name=store_contains)
            stocks = stocks.filter(store_name=store)

        return stocks


class StockUpdateView(LoginRequiredMixin, UpdateView):
    form_class = StockForm
    model = Stock
    template_name = 'stocks/stock_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Stock'
        return context


class StockDeleteView(LoginRequiredMixin, DeleteView):
    model = Stock
    template_name = 'main/confirm_delete.html'
    success_url = '/stock_list'


def stock_update():
    buy = BuyVoucher.objects.all()

    for item in buy:
        if not item.weight_of_each_bag:
            item.weight_of_each_bag = 0
        Stock.objects.create(voucher_no=item, business_name=item.business_name,
                             product=item.product_name, weight=item.weight,
                             rate_per_kg=item.rate_per_kg, rate_per_mann=item.rate_per_mann,
                             number_of_bag=item.number_of_bag, weight_of_bags=item.weight_of_each_bag,
                             added_by=item.added_by, date_time_stamp=item.date_time_stamp,
                             )
        print('stock updated:'+ str(item.id))

