from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView
from django.forms import formset_factory, inlineformset_factory
from .forms import HutBuyForm, ProductForm, ExpenseForm
from .models import HutBuy


@login_required
def hut_buy_create(request):
    form1 = HutBuyForm(request.POST or None)
    product_set = formset_factory(ProductForm)
    # expense_set = formset_factory(ExpenseForm)
    form2set = product_set(request.POST or None, request.FILES)
    # form3set = expense_set(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form1.is_valid():
            buy = form1.save(commit=False)
            buy.posted_by = request.user
            buy.save()
            for form2 in form2set:
                product = form2.save(commit=False)
                product.hut_buy = buy
                # product.save()
                print(product)
            # for form3 in form3set:
            #     expense = form3.save(commit=False)
            #     expense.hut_buy = buy
            #     expense.save()
            #     print(expense)
            return redirect('/hut_buy_list')
    else:
        form1 = HutBuyForm
        form2set = product_set
        # form3set = expense_set

    context = {
        'form1': form1,
        'form2set': form2set,
        # 'form3set': form3set,
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