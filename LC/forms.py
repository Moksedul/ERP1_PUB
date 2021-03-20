from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm
from .models import LC, LCProduct, LCExpense


class LCForm(ModelForm):
    class Meta:
        model = LC
        fields = '__all__'
        exclude = ('added_by', 'date_time_stamp')
        widgets = {
                    'opening_date': AdminDateWidget(),
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['sale_no'].widget.attrs['readonly'] = True


class ProductForm(ModelForm):
    class Meta:
        model = LCProduct
        fields = '__all__'
        exclude = ('lc',)
        labels = {
            'name': 'Product Name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ExpenseForm(ModelForm):
    class Meta:
        model = LCExpense
        fields = '__all__'
        exclude = ('lc',)
        labels = {
            'name': 'Expense Name',
            'amount': 'Expense Amount',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)