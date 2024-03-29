from django.forms import ModelForm, CheckboxSelectMultiple

from stocks.models import PreStock, FinishedStock, ProcessingStock, PostStock


class PreStockForm(ModelForm):

    class Meta:
        model = PreStock
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_no'].disabled = True
        if self.instance.voucher_no:
            self.fields['business_name'].disabled = True


class PreStockFormBuy(ModelForm):

    class Meta:
        model = PreStock
        fields = ('product', 'weight', 'weight_adjustment', 'rate_per_kg',
                  'rate_per_mann', 'number_of_bag', 'weight_of_bags', 'store_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProcessingStockForm(ModelForm):

    class Meta:
        model = ProcessingStock
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self_object = ProcessingStock.objects.get(id=self.instance.id)
        self.fields['pre_processing_stocks'].widget = CheckboxSelectMultiple()
        self.fields['pre_processing_stocks'].queryset = self_object.pre_processing_stocks.all()


class PostStockForm(ModelForm):
    class Meta:
        model = PostStock
        fields = '__all__'


class FinishedStockForm(ModelForm):

    class Meta:
        model = FinishedStock
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['pre_stock'].disabled = True
        # if self.instance.voucher_no:
        #     self.fields['business_name'].disabled = True