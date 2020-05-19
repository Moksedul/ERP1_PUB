from django.forms import ModelForm
from .models import Products


class ProductFrom(ModelForm):
    class Meta:
        model = Products
        fields = '__all__'