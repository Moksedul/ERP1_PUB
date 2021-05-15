from django.forms import ModelForm, TextInput
from django.contrib.admin.widgets import AdminDateWidget
from .models import Challan


class ChallanForm(ModelForm):
    class Meta:
        model = Challan
        fields = '__all__'
        exclude = ('added_by', 'date_added',)
        widgets = {
            'challan_date': AdminDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['challan_no'].widget.attrs['readonly'] = True
