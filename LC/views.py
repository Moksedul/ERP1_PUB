
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, inlineformset_factory

from django.shortcuts import render, redirect

from django.utils.timezone import now
from django.views.generic import ListView, DeleteView

from LC.forms import LCForm, ProductForm, ExpenseForm
from LC.models import LC, LCProduct, LCExpense
from organizations.models import Bank


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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lc_selection = LC.objects.all()
        banks = Bank.objects.all()

        lc_contains = self.request.GET.get('lc_number')
        if lc_contains is None:
            lc_contains = 'Select Lc Number'

        bank_contains = self.request.GET.get('bank')

        if bank_contains is None or bank_contains == '' or bank_contains == 'Select Bank':
            bank = 'Select Bank'
        else:
            bank = Bank.objects.get(id=bank_contains)

        order_contains = self.request.GET.get('order_by')
        if order_contains is None:
            order_contains = 'Select Order'

        today = now()

        context['banks'] = banks
        context['lc_selected'] = lc_contains
        context['lc_selection'] = lc_selection
        context['bank_selected'] = bank
        context['order_selected'] = order_contains
        context['tittle'] = 'techAlong Business|LC List'
        context['today'] = today
        return context

    def get_queryset(self):
        order_contains = self.request.GET.get('order_by')

        if order_contains is None:
            order_contains = 'Select Order'
            lc = LC.objects.all().order_by('-date_time_stamp')
        elif order_contains == 'LC Number':
            lc = LC.objects.all().order_by('lc_number')
        elif order_contains == 'Bank':
            lc = LC.objects.all().order_by('bank_name')
        else:
            lc = LC.objects.all().order_by('-opening_date')

        lc_contains = self.request.GET.get('lc_number')
        if lc_contains is None:
            lc_contains = 'Select Lc Number'

        bank_contains = self.request.GET.get('bank')
        if bank_contains is None:
            bank_contains = 'Select Bank'

        # checking bank_name from input
        if bank_contains != 'Select Bank' and bank_contains !='':
            lc = lc.filter(bank_name=bank_contains)

        # checking lc number from input
        if lc_contains != '' and lc_contains != 'Select Lc Number':
            lc = lc.filter(lc_number=lc_contains)
        print(lc.count())
        return lc


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
