from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from .models import BkashTransaction, PaymentBkashAgent


class TransactionForm(ModelForm):
    class Meta:
        model = BkashTransaction
        fields = '__all__'
        exclude = ('posted_by', 'date_time_stamp',)
        widgets = {
            'transaction_date': AdminDateWidget(),
        }
        # labels = {
        #     'date': 'Transaction Date',
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice_no'].widget.attrs['readonly'] = True
