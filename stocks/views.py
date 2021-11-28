from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from organizations.models import Organization
from products.models import Products
from vouchers.models import BuyVoucher
from .forms import PreStockForm, FinishedStockForm, ProcessingStockForm
from .models import PreStock, Store, FinishedStock, ProcessingStock


# Create your views here.
class StockCreateView(LoginRequiredMixin, CreateView):
    form_class = PreStockForm
    template_name = 'stocks/pre_stock_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Save'
        context['tittle'] = 'Add Stock'
        return context


def stock_view(request):
    stocks = PreStock.objects.all()
    all_weights = []
    for stock in stocks:
        all_weights.append(stock.weight)
    total_weight = sum(all_weights)
    context = {"total_weight": int(total_weight)}
    return render(request, 'stocks/report.html', context)


class StockListView(LoginRequiredMixin, ListView):
    model = PreStock
    template_name = 'stocks/pre_stock_list.html'
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
        stocks = PreStock.objects.all().order_by('-last_updated_time')
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
    form_class = PreStockForm
    model = PreStock
    template_name = 'stocks/pre_stock_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Stock'
        return context


class StockDeleteView(LoginRequiredMixin, DeleteView):
    model = PreStock
    template_name = 'main/confirm_delete.html'
    success_url = '/pre_stock_list'


class ProcessingStockCreate(LoginRequiredMixin, CreateView):
    form_class = ProcessingStockForm
    template_name = 'stocks/processing_stock_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Save'
        context['tittle'] = 'Add Processing Stock'
        return context


class ProcessingStockList(LoginRequiredMixin, ListView):
    model = ProcessingStock
    template_name = 'stocks/processing_stock_list.html'
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
        context['tittle'] = 'Processing Stock List'
        return context

    def get_queryset(self):
        stocks = ProcessingStock.objects.all().order_by('-last_updated_time')
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


class ProcessingStockUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProcessingStockForm
    model = ProcessingStock
    template_name = 'stocks/processing_stock_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Processing Stock'
        return context


class ProcessingStockDelete(LoginRequiredMixin, DeleteView):
    model = ProcessingStock
    template_name = 'main/confirm_delete.html'
    success_url = '/stock_processing_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Processing Stock'
        context['tittle'] = 'Delete Processing Stock'
        context['cancel_url'] = '/stock_processing_list'
        return context


@login_required()
def load_processing_stock(request):
    processing_stocks = ProcessingStock.objects.all()

    return render(request, 'stocks/processing_stock_options.html', context={'existing_stocks': processing_stocks})


@login_required()
def processing_stock_mess_creation(request):

    selected_pre_stocks = request.POST.getlist('selected_pre_stock')
    selected_member = request.POST.get('selected_member')

    print(selected_pre_stocks)

    return redirect(ProcessingStock)


class FinishedStockCreate(LoginRequiredMixin, CreateView):
    form_class = FinishedStockForm
    template_name = 'stocks/finished_stock_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Save'
        context['tittle'] = 'Add Finished Stock'
        return context


class FinishedStockList(LoginRequiredMixin, ListView):
    model = FinishedStock
    template_name = 'stocks/finished_stock_list.html'
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
        context['tittle'] = 'Processing Stock List'
        return context

    def get_queryset(self):
        stocks = FinishedStock.objects.all().order_by('-last_updated_time')
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


class FinishedStockUpdate(LoginRequiredMixin, UpdateView):
    form_class = FinishedStockForm
    model = FinishedStock
    template_name = 'stocks/finished_stock_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Finished Stock'
        return context


class FinishedStockDelete(LoginRequiredMixin, DeleteView):
    model = FinishedStock
    template_name = 'main/confirm_delete.html'
    success_url = '/finished_stock_list'


def stock_update():
    buy = BuyVoucher.objects.all()

    for item in buy:
        if not item.weight_of_each_bag:
            item.weight_of_each_bag = 0
        PreStock.objects.create(voucher_no=item, business_name=item.business_name,
                                product=item.product_name, weight=item.weight,
                                rate_per_kg=item.rate_per_kg, rate_per_mann=item.rate_per_mann,
                                number_of_bag=item.number_of_bag, weight_of_bags=item.weight_of_each_bag,
                                added_by=item.added_by, date_time_stamp=item.date_time_stamp,
                                )
        print('stock updated:'+ str(item.id))

