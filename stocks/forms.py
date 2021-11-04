from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
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
        fields = ('product', 'weight', 'weight_adjustment', 'rate', 'number_of_bag')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = "text-left"
        # self.helper.field_class = "col-md-12"
        self.helper.layout = Layout(
            Div(
                (Div(Field('product'), css_class='col-md-4')), (Div(Field('weight'), css_class='col-md-4')), css_class='row')
            )
