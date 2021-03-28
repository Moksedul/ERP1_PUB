from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import ListView, DeleteView, UpdateView

from LC.forms import LCForm, ProductForm, ExpenseForm
from LC.models import LC, LCProduct, LCExpense


@login_required
def lc_create(request):
    form1 = LCForm(request.POST or None, prefix='lc')
    product_set = formset_factory(ProductForm,)
    expense_set = formset_factory(ExpenseForm, extra=3)
    form2set = product_set(request.POST or None, request.FILES, prefix='product')
    form3set = expense_set(request.POST or None, request.FILES, prefix='expense')
    if request.method == 'POST':
        if form1.is_valid():
            lc = form1.save(commit=False)
            lc.added_by = request.user
            print(lc)
            lc.save()
            for form2 in form2set:
                product = form2.save(commit=False)
                product.lc = lc
                product.save()

            for form3 in form3set:
                expense = form3.save(commit=False)
                expense.lc = lc
                expense.save()
            return redirect('/lc_list')
    else:
        form1 = LCForm(prefix='lc')
        form2set = product_set(prefix='product')
        form3set = expense_set(prefix='expense')

    context = {
        'form1': form1,
        'form2set': form2set,
        'form3set': form3set,
        'form_name': 'LC Opening',
        'tittle': 'TAB | LC Opening',
        'button_name': 'Save',
    }

    return render(request, 'lc/lc_form.html', context)


class LCList(LoginRequiredMixin, ListView):
    model = LC
    template_name = 'lc/lc_list.html'
    context_object_name = 'lc'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now()
        context['tittle'] = 'techAlong Business|LC List'
        context['today'] = today
        return context


class LCDelete(LoginRequiredMixin, DeleteView):
    model = LC
    template_name = 'main/confirm_delete.html'
    success_url = '/lc_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'LC'
        context['tittle'] = 'LC Delete'
        context['cancel_url'] = '/lc_list'
        return context


@login_required
def lc_update(request, pk):
    buy = LC.objects.get(pk=pk)
    form1 = LCForm(instance=buy)
    ProductFormSet = inlineformset_factory(
                    LC, LCProduct, fields=('name', 'weight', 'rate', 'bags'), extra=1
                    )
    ExpenseFormSet = inlineformset_factory(
        LC, LCExpense, fields=('name', 'amount',), extra=1
    )
    form2set = ProductFormSet(instance=buy)
    form3set = ExpenseFormSet(instance=buy)
    if request.method == 'POST':
        form1 = LCForm(request.POST or None, instance=buy)
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
            return redirect('/lc_list')
    else:
        form1 = form1
        form2set = form2set
        form3set = form3set

    context = {
        'form1': form1,
        'form2set': form2set,
        'form3set': form3set,
        'form_name': 'LC Update',
        'button_name': 'Update',
        'tittle': 'techAlong Business|LC Update',
    }

    return render(request, 'lc/lc_form.html', context)
