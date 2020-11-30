from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django_select2.forms import Select2Widget

from organizations.models import Persons
from .models import Payment, BuyVoucher


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ('payed_by', 'transaction',)
        widgets = {
            'payment_date': AdminDateWidget(),
            'cheque_date': AdminDateWidget(),
            'payment_for_person': Select2Widget
        }
        labels = {
            'cheque_PO_ONL_no': 'Cheque/PO/ONL No',
            'cheque_date': 'Date',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['voucher_no'].queryset = BuyVoucher.objects.none()
        self.fields['payment_mode'].widget.attrs.update({'onchange': 'showChequeDetails()'})
        self.fields['payment_no'].widget.attrs['readonly'] = True

        if 'payment_for_person' in self.data:
            try:
                name = int(self.data.get('payment_for_person'))
                self.fields['voucher_no'].queryset = BuyVoucher.objects.filter(
                    seller_name=name).order_by('voucher_number')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Voucher queryset
        # elif self.instance.pk:
        #     self.fields['voucher_no'].queryset = self.instance.voucher_number.voucher_no_set.order_by('voucher_number')
        #
        # self.fields['payment_for_person'].queryset = Persons.objects.none()
        #
        # if 'payment_for_person' in self.data:
        #     self.fields['payment_for_person'].queryset = Persons.objects.all()
        #
        # elif self.instance.pk:
        #     self.fields['payment_for_person'].queryset = Persons.objects.all().filter(pk=self.instance.Persons.pk)
