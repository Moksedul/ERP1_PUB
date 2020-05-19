from django.shortcuts import render
from .forms import ProductFrom
from django_tables2 import SingleTableView
from .models import Products
from .table import ProductTable


# Create your views here.
def add_product(request):
    form = ProductFrom()
    if request.method == 'POST':
        form = ProductFrom(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'products/product_add.html', context)


class ProductListView(SingleTableView):
    model = Products
    table_class = ProductTable
    template_name = 'products/product_list.html'