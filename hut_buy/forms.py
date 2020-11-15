from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm
from .models import HutBuy, HutProduct, Expense


class HutBuyForm(ModelForm):
    class Meta:
        model = HutBuy
        fields = '__all__'
        exclude = ('posted_by', 'date_time_stamp')
        widgets = {
                    'date': AdminDateWidget(),
                }
        labels = {
            'sale_no': 'Voucher No',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['sale_no'].widget.attrs['readonly'] = True


class ProductForm(ModelForm):
    class Meta:
        model = HutProduct
        fields = '__all__'
        exclude = ('hut_buy',)
        labels = {
            'name': 'Product Name',
            'number_of_bag': 'Bags',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        exclude = ('hut_buy',)
        labels = {
            'name': 'Expense Name',
            'amount': 'Expense Amount',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)