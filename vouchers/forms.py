from django.forms import ModelForm
from django import forms
from .models import BuyVoucher


class BuyVoucherCreateFrom(ModelForm):

    class Meta:
        model = BuyVoucher
        fields = '__all__'