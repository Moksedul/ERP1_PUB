from django.db import models
from django.utils.timezone import now


class Employee(models.Model):
    employee_name = models.CharField(max_length=50)
    fathers_name = models.CharField(max_length=50, null=True, blank=True)
    mothers_name = models.CharField(max_length=50, null=True, blank=True)
    spouse_name = models.CharField(max_length=50, null=True, blank=True)
    phone_no = models.CharField(max_length=11, null=True, blank=True)
    hourly_rate = models.FloatField()
    address = models.CharField(max_length=200, blank=True, null=True)
    joining_date = models.DateField(default=now)
    photo = models.ImageField(upload_to='employee_photo', default='default.jpg')
