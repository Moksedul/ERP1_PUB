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
from organizations.models import Persons


@login_required
def lc_create(request):
    form1 = LCForm(request.POST or None, prefix='lc')
    product_set = formset_factory(ProductForm,)
    expense_set = formset_factory(ExpenseForm,)
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
        voucher_selection = LC.objects.all()

        voucher_contains = self.request.GET.get('voucher_no')
        if voucher_contains is None:
            voucher_contains = 'Select Lc Number'
        bank_contains = self.request.GET.get('bank_name')
        if bank_contains is None:
            name_contains = 'Bank Name'

        today = now()

        context['names'] = names
        context['voucher_selected'] = voucher_contains
        context['voucher_selection'] = voucher_selection
        context['bank_typed'] = bank_contains

        context['tittle'] = 'techAlong Business|LC List'
        context['today'] = today
        return context

    def get_queryset(self):
        vouchers = LC.objects.all().order_by('-date_time_stamp')
        order = self.request.GET.get('orderby')
        voucher_contains = self.request.GET.get('voucher_no')
        if voucher_contains is None:
            voucher_contains = 'Select Lc Number'
        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'
        phone_no_contains = self.request.GET.get('phone_no')

        if phone_no_contains is None or phone_no_contains == '':
            phone_no_contains = 'Select Phone No'

        # checking name from input
        if name_contains != 'Select Name':
            person = Persons.objects.get(person_name=name_contains)
            vouchers = vouchers.filter(buyer_name=person.id)

        # checking phone no from input
        if phone_no_contains != 'Select Phone No' and phone_no_contains != 'None':
            person = Persons.objects.get(contact_number=phone_no_contains)
            vouchers = vouchers.filter(buyer_name=person.id)

        # checking voucher number from input
        if voucher_contains != '' and voucher_contains != 'Select Lc Number':
            vouchers = vouchers.filter(lc_number=voucher_contains)

        return vouchers


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
            print('ok')
            for form2 in form2set:
                print('ok go')
                # form2.save()

            if form2set.is_valid():
                form2set.save()
                print('ok3')
            if form3set.is_valid():
                print('ok2')
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
