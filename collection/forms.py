from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from .models import Collection


class CollectionFormSale(ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'
        exclude = ('local_sale_voucher_no', 'sale_type', 'collected_by',)
        widgets = {
            'collection_date': AdminDateWidget(),
            'cheque_date': AdminDateWidget(),
        }
        labels = {
            'cheque_PO_ONL_no': 'Cheque/PO/ONL No',
            'cheque_date': 'Date',
            'collection_status': 'Approve',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection_mode'].widget.attrs.update({'onchange': 'showChequeDetails()'})
        self.fields['collection_no'].widget.attrs['readonly'] = True


class CollectionFormLocalSale(ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'
        exclude = ('sale_voucher_no', 'sale_type', 'collected_by',)
        widgets = {
            'collection_date': AdminDateWidget(),
            'cheque_date': AdminDateWidget(),
        }
        labels = {
            'cheque_PO_ONL_no': 'Cheque/PO/ONL No',
            'cheque_date': 'Date',
            'collection_status': 'Approve',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection_mode'].widget.attrs.update({'onchange': 'showChequeDetails()'})
        self.fields['collection_no'].widget.attrs['readonly'] = True
