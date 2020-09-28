from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView

from .forms import SaleForm
from .models import LocalSale, Product


class SaleCreate(LoginRequiredMixin, CreateView):
    form_class = SaleForm
    template_name = 'local_sale/sale_add_form.html'
    success_url = '/add_local_sale'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        super().form_valid(form=form)
        print(form)
        return HttpResponseRedirect(self.get_success_url())


def sale_create(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.session['id'])
        form = SaleForm(request.POST)
        if form.is_valid():
            form.posted_by = user
            form.save()
            messages.success(request, f'Your Account Has Been Created ! You can now log in.')
            return redirect('/local_sale_list')
    else:
        form = SaleForm()
    return render(request, 'local_sale/sale_add_form.html', {'form': form})


class LocalSaleList(LoginRequiredMixin, ListView):
    model = LocalSale
    template_name = 'local_sale/sale_list.html'
    context_object_name = 'sales'
    paginate_by = 20
