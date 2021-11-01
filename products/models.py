from django.db import models
from django.urls import reverse


class Products(models.Model):
    product_name = models.CharField(max_length=200)
    product_category = models.CharField(max_length=200)

    class Meta:
        unique_together = [("product_name", "product_category")]

    def __str__(self):
        return str(self.product_name)

    @staticmethod
    def get_absolute_url():
        return reverse('product-list')
