from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm
from .models import Investment


class InvestmentForm(ModelForm):
    class Meta:
        model = Investment
        fields = ('source_of_investment', 'investing_amount', 'investing_from_account', 'investing_to_account', 'date', 'remarks',)
        widgets = {
                    'date': AdminDateWidget(),
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['sale_no'].widget.attrs['readonly'] = True