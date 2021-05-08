from PIL import Image
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
    contact_number = models.CharField(max_length=17, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    nid_photo = models.ImageField(upload_to='nid_photo', blank=True)
    person_photo = models.ImageField(upload_to='person_photo', default='default.jpg')

    def __str__(self):
        return str(self.person_name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.person_photo.path)
        if self.nid_photo:
            nid_img = Image.open(self.nid_photo.path)
            if nid_img.height > 207 or nid_img.width > 327:
                output_size = (207, 327)
                nid_img.thumbnail(output_size)
                nid_img.save(self.nid_photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.person_photo.path)

    @staticmethod
    def get_absolute_url():
        return reverse('person-list')


class Bank(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Organization(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)