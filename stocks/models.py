from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Products

CONDITION_CHOICES = [
    ('Processed', 'Processed'),
    ('Un Processed', 'Un Processed'),
]


class Stocks(models.Model):

    number_of_bag = models.FloatField()
    weight = models.FloatField()
    name_of_product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    product_condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, default='Processed')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remarks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.room_no)

    @staticmethod
    def get_absolute_url():
        return reverse('stock-list')