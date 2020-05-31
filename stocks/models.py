from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Products

CONDITION_CHOICES = [
    ('pr', 'Processed'),
    ('upr', 'Un Processed'),
]


# Create your models here. RoomNo,NumberOfBags,Weight,ProductId,ProductCondition,LastModifiedBy,CreatedBy,Remarks
class Stocks(models.Model):
    room_no = models.IntegerField()
    number_of_bag = models.FloatField()
    weight = models.FloatField()
    name_of_product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    product_condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, default='pr')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    remarks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.product_condition)

    @staticmethod
    def get_absolute_url():
        return reverse('add-stock')