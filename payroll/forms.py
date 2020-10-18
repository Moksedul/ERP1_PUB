from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, Div, HTML, Button
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
        self.fields['employee_name'].widget.attrs.update({'class': 'input-group-sm'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('employee_name', css_class='form-group col-md-4 mb-0'),
                Column('phone_no', css_class='form-group col-md-4 mb-0'),
                Column('hourly_rate', css_class='form-group col-md-2 mb-0'),
                Column('joining_date', css_class='form-group col-md-2 mb-0'),
                css_class='form-row input-small'
            ),
            Row(
                Column('fathers_name', css_class='form-group col-md-4 mb-0'),
                Column('mothers_name', css_class='form-group col-md-4 mb-0'),
                Column('spouse_name', css_class='form-group col-md-4 mb-0'),
            ),
            'address',
            Row(
              Column('photo', css_class='form-group col-md-4 mb-0')
            ),

            Submit('submit', 'Save'),
            Submit('submit', 'Save & Add Another'),
        )

        # self.fields['payment_no'].widget.attrs['readonly'] = True

