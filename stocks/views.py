from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from organizations.models import Organization
from products.models import Products
from vouchers.models import BuyVoucher
from .forms import PreStockForm, FinishedStockForm, ProcessingStockForm
from .models import PreStock, Store, FinishedStock, ProcessingStock, PostStock


# Create your views here.
class PreStockCreate(LoginRequiredMixin, CreateView):
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


def pre_stock_view(request):
    stocks = PreStock.objects.all()
    all_weights = []
    for stock in stocks:
        all_weights.append(stock.weight)
    total_weight = sum(all_weights)
    context = {"total_weight": int(total_weight)}
    return render(request, 'stocks/report.html', context)


class PreStockList(LoginRequiredMixin, ListView):
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
        context['tittle'] = 'Pre Stock List'
        return context

    def get_queryset(self):
        stocks = PreStock.objects.all().order_by('-date_time_stamp')
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


class PreStockUpdate(LoginRequiredMixin, UpdateView):
    form_class = PreStockForm
    model = PreStock
    template_name = 'stocks/pre_stock_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Pre Stock'
        return context


class PreStockDelete(LoginRequiredMixin, DeleteView):
    model = PreStock
    template_name = 'main/confirm_delete.html'
    success_url = '/pre_stock_list'


class ProcessingStockCreate(LoginRequiredMixin, CreateView):
    form_class = ProcessingStockForm
    template_name = 'stocks/processing_stock_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        pre_stocks = form.cleaned_data['pre_stocks']
        pre_stocks.update(added_to_processing_stock=True)
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
        stocks = ProcessingStock.objects.all().order_by('-date_time_stamp')
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
        weight = 0
        pre_stocks = self.object.pre_stocks.all()
        for pre_stock in pre_stocks:
            weight += pre_stock.details['net_weight']
        pre_stocks = pre_stocks.first()
        context['weight'] = weight
        context['pre_stocks'] = pre_stocks
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Processing Stock'
        return context


@login_required
def processing_stock_update(request, pk):
    pro_stock = ProcessingStock.objects.get(pk=pk)
    processing_form = ProcessingStockForm(instance=pro_stock)
    post_stock_set = inlineformset_factory(
        ProcessingStock, PostStock,
        fields=('business_name', 'product', 'weight', 'bags', 'rate_per_kg', 'store'), extra=0
    )
    post_stock_form_set = post_stock_set(instance=pro_stock)
    if request.method == 'POST':
        processing_form = ProcessingStockForm(request.POST or None, instance=pro_stock)
        post_stock_form_set = post_stock_set(request.POST, instance=pro_stock)
        if processing_form.is_valid():
            processing_form.save()
            if post_stock_form_set.is_valid():
                post_stock_form_set.save()
            return redirect('/stock_processing_list')
    else:
        processing_form = processing_form
        post_stock_form_set = post_stock_form_set

    context = {
        'processing_stock': pro_stock,
        'tittle': 'Processing Update',
        'form': processing_form,
        'form2set': post_stock_form_set,
        'button_name': 'Update',
        'formset_name': 'poststock_set',
    }
    return render(request, 'stocks/processing_stock_form.html', context=context)


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
    selected_processing_stock = request.POST.get('processing_stock')
    product_ids = []
    # same_products = None

    if selected_processing_stock:
        existing_processing_stock = ProcessingStock.objects.get(id=selected_processing_stock)
        pre_stocks_in_exs_pros = existing_processing_stock.pre_stocks.all()
        [product_ids.append(pre_stock.product.pk) for pre_stock in pre_stocks_in_exs_pros]
    else:
        existing_processing_stock = None

    if selected_pre_stocks:  # checking all selected products are same
        all_pre_stocks = PreStock.objects.filter(id__in=selected_pre_stocks)
        [product_ids.append(pre_stock.product.pk) for pre_stock in all_pre_stocks]
        same_products = all(value == product_ids[0] for value in product_ids)
    else:
        messages.warning(request, 'Please Select Some Products')
        return redirect(PreStock)

    if same_products and existing_processing_stock:
        for item in selected_pre_stocks:
            existing_processing_stock.pre_stocks.add(item)
        return redirect(PreStock)
    elif same_products and not existing_processing_stock:
        new_processing_stock = ProcessingStock()
        new_processing_stock.save()
        new_processing_stock.pre_stocks.set(selected_pre_stocks)
        return redirect(ProcessingStock)
    else:
        messages.warning(request, " Selected Product's are not Same")
        return redirect(PreStock)


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
        context['tittle'] = 'Finished Stock List'
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
        print('stock updated:' + str(item.id))


def processing_complete(request, pk, pro_id):

    def create_fs(processed_stock):
        FinishedStock.objects.create(business_name=processed_stock.business_name,
                                     rate_per_kg=processed_stock.rate_per_kg, weight=processed_stock.weight,
                                     number_of_bag=processed_stock.bags,
                                     product=processed_stock.product,
                                     processing_stock=processed_stock.processing_stock
                                     )

    if pk is not 0 and pro_id is 0:
        processing_stock = ProcessingStock.objects.get(id=pk)
        processed_products = PostStock.objects.filter(processing_stock=processing_stock, is_finished=False)

        if processed_products.exists():
            for processed_product in processed_products:
                try:
                    create_fs(processed_product)
                    processed_product.is_finished = True
                    processed_product.save()
                    messages.success(request, "Processing Completed and items are added to Finished Stock")
                except:
                    messages.error(request, "Already Finished!")
                    return redirect('processing-stock-update', pk)
        else:
            messages.error(request, "All are Already Finished!")
            return redirect('processing-stock-update', pk)
        return redirect(FinishedStock)

    elif pk is not 0 and pro_id is not 0:
        processed_product = PostStock.objects.get(id=pro_id)
        create_fs(processed_product)
        processed_product.is_finished = True
        processed_product.save()
        messages.success(request, "Processing Completed and Selected item is added to Finished Stock")
        return redirect('processing-stock-update', pk)


def post_stock_is_completed(request):
    post_stock_id = request.GET.get('post_stock')
    post_stock = PostStock.objects.get(id=post_stock_id)
    return JsonResponse({"is_completed": post_stock.is_finished})
