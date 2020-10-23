from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.forms import ModelForm, TimeInput, BaseInlineFormSet
from django.contrib.admin.widgets import AdminDateWidget
from .models import Employee, Attendance, Day, TimeTable


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
                Column('employee_name', css_class='form-group col-md-3 mb-0'),
                Column('designation', css_class='form-group col-md-3 mb-0'),
                Column('phone_no', css_class='form-group col-md-2 mb-0'),
                Column('hourly_rate', css_class='form-group col-md-2 mb-0'),
                Column('joining_date', css_class='form-group col-md-2 mb-0'),
            ),
            Row(
                Column('fathers_name', css_class='form-group col-md-3 mb-0'),
                Column('mothers_name', css_class='form-group col-md-3 mb-0'),
                Column('spouse_name', css_class='form-group col-md-3 mb-0'),
                Column('NID', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('address', css_class='form-group col-md-10 mb-0'),
                Column('time_table', css_class='form-group col-md-2 mb-0')
            ),
            Row(
              Column('photo', css_class='form-group col-md-4 mb-0')
            ),

            Submit('submit', 'Save'),
        )


class DayForm(ModelForm):
    class Meta:
        model = Day
        fields = '__all__'
        widgets = {
            'date': AdminDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0'),
            ),
            Submit('submit', 'Create'),
        )


class TimeTableForm(ModelForm):
    class Meta:
        model = TimeTable
        fields = '__all__'
        widgets = {
            'in_time': TimeInput(attrs={'type': 'time'}),
            'out_time': TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('time_table_name', css_class='form-group col-md-4 mb-0'),
                Column('in_time', css_class='form-group col-md-4 mb-0'),
                Column('out_time', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
               'weekend'
            ),
            Submit('submit', 'Save'),
        )