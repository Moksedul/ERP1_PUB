from django import forms
from django.forms import ModelForm
from .models import Products


class ProductFrom(ModelForm):
    product_category = forms.CharField(required=False)

    class Meta:
        model = Products
        fields = '__all__'