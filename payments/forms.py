from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from .models import Payment


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'payment_date': AdminDateWidget(),
            'cheque_date': AdminDateWidget(),
        }
        labels = {
            'cheque_PO_ONL_no': 'Cheque/PO/ONL No',
            'cheque_date': 'Date',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_mode'].widget.attrs.update({'onchange': 'showChequeDetails()'})
        self.fields['payment_no'].widget.attrs['readonly'] = True

