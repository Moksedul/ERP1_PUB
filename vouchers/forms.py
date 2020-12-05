from django.forms import ModelForm, Textarea
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_number'].widget.attrs['readonly'] = True


class GeneralForm(ModelForm):
    class Meta:
        model = GeneralVoucher
        fields = '__all__'
        exclude = ('transaction',)
        widgets = {
            'date_added': AdminDateWidget(),
        }
