from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView
from django.forms import formset_factory, inlineformset_factory
from .forms import HutBuyForm, ProductForm, ExpenseForm
from .models import HutBuy, HutProduct, Expense


@login_required
def hut_buy_create(request):
    form1 = HutBuyForm(request.POST or None, prefix='hut')
    product_set = formset_factory(ProductForm)
    expense_set = formset_factory(ExpenseForm)
    form2set = product_set(request.POST or None, request.FILES, prefix='product')
    form3set = expense_set(request.POST or None, request.FILES, prefix='expense')
    if request.method == 'POST':
        if form1.is_valid():
            buy = form1.save(commit=False)
            buy.posted_by = request.user
            print(buy)
            buy.save()
            for form2 in form2set:
                product = form2.save(commit=False)
                print(product)
                product.hut_buy = buy
                product.save()

            for form3 in form3set:
                expense = form3.save(commit=False)
                expense.hut_buy = buy
                expense.save()
                print(expense)
            return redirect('/hut_buy_list')
    else:
        form1 = HutBuyForm(prefix='hut')
        form2set = product_set(prefix='product')
        form3set = expense_set(prefix='expense')

    context = {
        'form1': form1,
        'form2set': form2set,
        'form3set': form3set,
        'form_name': 'Hut-Buy Add',
        'button_name': 'Save',
    }

    return render(request, 'hut_buy/hut_buy_form.html', context)


class HutBuyList(LoginRequiredMixin, ListView):
    model = HutBuy
    template_name = 'hut_buy/hut_buy_list.html'
    context_object_name = 'hut_buy'


class HutBuyDelete(LoginRequiredMixin, DeleteView):
    model = HutBuy
    template_name = 'main/confirm_delete.html'
    success_url = '/hut_buy_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Hut Buy'
        context['cancel_url'] = '/hut_buy_list'
        return context


@login_required
def hut_buy_update(request, pk):
    buy = HutBuy.objects.get(pk=pk)
    form1 = HutBuyForm(instance=buy)
    ProductFormSet = inlineformset_factory(
                    HutBuy, HutProduct, fields=('name', 'weight', 'price'), extra=1
                    )
    ExpenseFormSet = inlineformset_factory(
        HutBuy, Expense, fields=('name', 'amount',), extra=1
    )
    form2set = ProductFormSet(instance=buy)
    form3set = ExpenseFormSet(instance=buy)
    if request.method == 'POST':
        form1 = HutBuyForm(request.POST or None, instance=buy)
        form2set = ProductFormSet(request.POST, instance=buy)
        form3set = ExpenseFormSet(request.POST, instance=buy)
        if form1.is_valid():
            buy = form1.save(commit=False)
            buy.posted_by = request.user
            buy.save()
            if form2set.is_valid():
                form2set.save()
            if form3set.is_valid():
                form3set.save()
            return redirect('/hut_buy_list')
    else:
        form1 = form1
        form2set = form2set
        form3set = form3set

    context = {
        'form1': form1,
        'form2set': form2set,
        'form3set': form3set,
        'form_name': 'Hut-Buy Update',
        'button_name': 'Update',
    }

    return render(request, 'hut_buy/hut_buy_form.html', context)


@login_required
def hut_buy_detail(request, pk):

    context = {
        'button_name': 'Update',
    }

    return render(request, 'hut_buy/hut_buy_detail.html', context)
