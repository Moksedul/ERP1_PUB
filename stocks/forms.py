from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django.forms import ModelForm

from stocks.models import Stock


class StockForm(ModelForm):

    class Meta:
        model = Stock
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_no'].disabled = True
        if self.instance.voucher_no:
            self.fields['business_name'].disabled = True


class StockFormBuy(ModelForm):

    class Meta:
        model = Stock
        fields = ('product', 'weight', 'weight_adjustment', 'rate_per_kg',
                  'rate_per_mann', 'number_of_bag', 'weight_of_bags', 'store_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
