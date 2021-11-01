from crispy_forms.helper import FormHelper
from django.forms import ModelForm

from stocks.models import Stocks


class StockForm(ModelForm):

    class Meta:
        model = Stocks
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_no'].widget.attrs['disabled'] = 'disabled'
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
