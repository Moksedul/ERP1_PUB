from django.forms import ModelForm
from .models import Payment


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_no'].widget.attrs.update({'class': 'special'})
        self.fields['payment_mode'].widget.attrs.update({'onchange': 'myFunction()'})
