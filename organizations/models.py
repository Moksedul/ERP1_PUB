from django.db import models
from django.urls import reverse


class Companies(models.Model):
    name_of_company = models.CharField(max_length=200, unique=True)
    company_address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name_of_company)

    @staticmethod
    def get_absolute_url():
        return reverse('company-list')


# Create your models here. PersonName,CompanyName,Address,NID,ContactNumber,Email,NIDPhoto
class Persons(models.Model):
    person_name = models.CharField(max_length=200)
    company_name = models.ForeignKey(Companies, null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, blank=True)
    nid = models.CharField(max_length=20, blank=True, unique=True, null=True)
    contact_number = models.CharField(max_length=17, unique=True, null=True)
    email = models.EmailField(max_length=50, blank=True)
    nid_photo = models.ImageField(upload_to='nid_photo', blank=True)

    def __str__(self):
        return str(self.person_name)

    @staticmethod
    def get_absolute_url():
        return reverse('person-list')