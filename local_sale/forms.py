from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm
from local_sale.models import LocalSale


class SaleForm(ModelForm):
    class Meta:
        model = LocalSale
        fields = '__all__'
        exclude = ('posted_by', 'date_time_stamp')
        widgets = {
                    'date': AdminDateWidget(),
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sale_no'].widget.attrs['readonly'] = True
