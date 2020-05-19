import django_tables2 as tables
from .models import Products


class ProductTable(tables.Table):
    class Meta:
        model = Products
        template_name = 'django_tables2/bootstrap.html'
        fields = ('product_name', 'product_category')