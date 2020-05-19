from django.db import models


# Create your models here.
class Products(models.Model):
    product_name = models.CharField(max_length=200)
    product_category = models.CharField(max_length=200)

    def __str__(self):
        return self.product_name, self.product_category
