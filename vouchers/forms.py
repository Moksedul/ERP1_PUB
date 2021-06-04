from django.forms import ModelForm, Textarea
from django.contrib.admin.widgets import AdminDateWidget
from .models import *


class SaleForm(ModelForm):
    class Meta:
        model = SaleVoucher
        fields = '__all__'
        exclude = ('date_time_stamp',)
        widgets = {
            'date_added': AdminDateWidget(),
        }
        labels = {
            'status': 'Confirm',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_number'].widget.attrs['readonly'] = True


class ExpenseForm(ModelForm):
    class Meta:
        model = SaleExpense
        fields = '__all__'
        exclude = ('sale',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BuyForm(ModelForm):
    class Meta:
        model = BuyVoucher
        fields = '__all__'
        exclude = ('date_time_stamp',)
        widgets = {
            'date_added': AdminDateWidget(),
        }

        labels = {
            'number_of_vehicle': 'গাড়ির সংখ্যা',
            'rate_per_kg': 'মূল্য/কেজি',
            'rate_per_mann': 'মূল্য/মণ',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_number'].widget.attrs['readonly'] = True


class GeneralForm(ModelForm):
    class Meta:
        model = GeneralVoucher
        fields = '__all__'
        exclude = ('transaction',)
        labels = {
            'cost_amount': 'Amount'
        }
        widgets = {
            'date_added': AdminDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_number'].widget.attrs['readonly'] = True