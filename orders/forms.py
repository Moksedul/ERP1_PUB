from django.forms import ModelForm
from .models import Orders


class OrderForm(ModelForm):
    model = Orders

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_no'].disabled = True

    class Meta:
        fields = ('order_no', 'person_name', 'company_name',
                  'product_name', 'total_weight', 'rate_per_kg', 'percentage_of_fotka', 'percentage_of_moisture',
                  'delivery_deadline', 'date_ordered', 'remarks',)
