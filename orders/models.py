from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from products.models import Products
from organizations.models import Persons, Companies

ORDER_STATUS_CHOICES = [
    ('Processing', 'Processing'),
    ('Confirmed', 'Confirmed'),
    ('Delivered', 'Delivered'),
]


def increment_order_number():
    last_order = Orders.objects.all().order_by('id').last()
    if not last_order:
        return 'FEO-0001'
    order_number = last_order.order_no
    order_int = int(order_number.split('FEO-')[-1])
    new_order_int = order_int + 1
    new_order_no = ''
    if new_order_int < 10:
        new_order_no = 'FEO-000' + str(new_order_int)
    if 100 > new_order_int >= 10:
        new_order_no = 'FEO-00' + str(new_order_int)
    if 100 <= new_order_int < 1000:
        new_order_no = 'FEO-0' + str(new_order_int)
    if new_order_int >= 1000:
        new_order_no = 'FEO-' + str(new_order_int)
    return new_order_no


# model for order
class Orders(models.Model):
    order_no = models.CharField(max_length=10, unique=True, default=increment_order_number)
    person_name = models.ForeignKey(Persons, on_delete=models.CASCADE, null=True)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    total_weight = models.FloatField(max_length=10)
    rate_per_kg = models.FloatField(max_length=10)
    percentage_of_fotka = models.FloatField(max_length=10)
    percentage_of_moisture = models.FloatField(max_length=10)
    delivery_deadline = models.DateField(default=now)
    date_ordered = models.DateTimeField(default=now)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=20, null=True, choices=ORDER_STATUS_CHOICES, default='Processing')
    remarks = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.order_no)

    @staticmethod
    def get_absolute_url():
        return reverse('order-list')