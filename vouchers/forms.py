from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from .models import *


class SaleForm(ModelForm):
    class Meta:
        model = SaleVoucher
        fields = '__all__'
        widgets = {
            'date_added': AdminDateWidget(),
        }
        labels = {
            'status': 'Confirm',
        }


class BuyForm(ModelForm):
    class Meta:
        model = BuyVoucher
        fields = '__all__'
        widgets = {
            'date_added': AdminDateWidget(),
        }