from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from .models import Employee


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'joining_date': AdminDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['payment_no'].widget.attrs['readonly'] = True

