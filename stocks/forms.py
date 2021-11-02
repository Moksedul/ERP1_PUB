from crispy_forms.helper import FormHelper
from django.forms import ModelForm

from stocks.models import YardStock


class StockForm(ModelForm):

    class Meta:
        model = YardStock
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_no'].widget.attrs['disabled'] = 'disabled'


class StockFormBuy(ModelForm):

    class Meta:
        model = YardStock
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_no'].widget.attrs['disabled'] = 'disabled'
