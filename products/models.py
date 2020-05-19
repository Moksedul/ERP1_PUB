from django.db import models


# Create your models here.
class Products(models.Model):
    product_name = models.CharField(label='Product Name', max_length=200)
    product_category = models.CharField(label='Product Category', max_length=200)

