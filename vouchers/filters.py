import django_filters
from .models import BuyVoucher


class BuyFilter(django_filters.FilterSet):

    class Meta:
        model = BuyVoucher
        fields = ('seller_name',)
