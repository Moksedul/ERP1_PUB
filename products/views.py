from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ProductFrom
from .models import Products


# Create your views here.
@login_required()
def add_product(request):
    form = ProductFrom()
    if request.method == 'POST':
        form = ProductFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/product_list')
    context = {'form': form}
    return render(request, 'products/product_add.html', context)


class ProductListView(LoginRequiredMixin, ListView):
    model = Products
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    # products = Products.objects.all()
    # return render(request, 'products/buy_list.html', {'products': products})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Products
    fields = ['product_name', 'product_category']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Products
    success_url = '/product_list'
