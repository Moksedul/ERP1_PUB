from django.db import models


# Create your models here. PersonName,CompanyName,Address,NID,ContactNumber,Email,NIDPhoto
class Organizations(models.Model):
    person_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=500, blank=True)
    nid = models.CharField(max_length=20, blank=True, unique=True, null=True)
    contact_number = models.CharField(max_length=17, unique=True, null=True)
    email = models.EmailField(max_length=50, blank=True)
    nid_photo = models.ImageField(upload_to='nid_photo')
