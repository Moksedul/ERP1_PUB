from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView

from LC.forms import LCForm, ProductForm, ExpenseForm
from LC.models import LC


@login_required
def lc_create(request):
    form1 = LCForm(request.POST or None, prefix='lc')
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
            return redirect('/lc_list')
    else:
        form1 = LCForm(prefix='hut')
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
    template_name = 'hut_buy/hut_buy_list.html'
    context_object_name = 'lc'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'techAlong Business|Hut Buy List'

        return context