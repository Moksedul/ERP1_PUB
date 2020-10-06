from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime

from challan.models import Challan
from local_sale.models import LocalSale
from vouchers.models import SaleVoucher
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
        self.fields['sale_voucher_no'].queryset = SaleVoucher.objects.none()
        self.fields['collection_mode'].widget.attrs.update({'onchange': 'showChequeDetails()'})
        self.fields['collection_no'].widget.attrs['readonly'] = True

        if 'collected_from' in self.data:
            try:
                name = int(self.data.get('collected_from'))
                challan = Challan.objects.filter(buyer_name=name)
                v_id = []
                for challan in challan:
                    sale = SaleVoucher.objects.get(challan_no_id=challan.id)
                    v_id.append(sale.voucher_number)
                self.fields['sale_voucher_no'].queryset = SaleVoucher.objects.filter(
                    voucher_number__in=v_id).order_by('voucher_number')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Voucher queryset
        # elif self.instance.pk:
        #     self.fields['voucher_no'].queryset = self.instance.voucher_number.voucher_no_set.order_by('voucher_number')


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
        # self.fields['local_sale_voucher_no'].queryset = LocalSale.objects.none()
        self.fields['collection_mode'].widget.attrs.update({'onchange': 'showChequeDetails()'})
        self.fields['collection_no'].widget.attrs['readonly'] = True

        if 'collected_from' in self.data:
            try:
                name = int(self.data.get('collected_from'))
                self.fields['local_sale_voucher_no'].queryset = LocalSale.objects.filter(
                    buyer_name=name).order_by('sale_no')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Voucher queryset
        # elif self.instance.pk:
        #     self.fields['voucher_no'].queryset = self.instance.voucher_number.voucher_no_set.order_by('voucher_number')
