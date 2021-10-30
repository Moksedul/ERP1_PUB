from django.forms import ModelForm

from stocks.models import Stocks


class StockForm(ModelForm):

    class Meta:
        model = Stocks
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_no'].widget.attrs['disabled'] = 'disabled'
