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

    @property
    def details(self):
        from core.views import product_details
        return product_details(self.pk)
    # def save(self, *args, **kwargs):
    #     items = Products.objects.filter(product_name=self.product_name)
    #     if items:  # if some items are found in the database
    #         items.update(product_category=self.product_category)
    #     else:
    #         return super(Products, self).save(*args, **kwargs)
