from PIL import Image
from django.db import models
from django.urls import reverse


class Companies(models.Model):
    name_of_company = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=200, default='Contact Person')
    designation = models.CharField(max_length=200, default='Designation')
    company_address = models.TextField(max_length=250)

    def __str__(self):
        return str(self.name_of_company)

    @staticmethod
    def get_absolute_url():
        return reverse('company-list')


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
    proprietor = models.CharField(max_length=50, default='N/A')
    signature = models.ImageField(upload_to='company_docs', blank=True)
    pad = models.ImageField(upload_to='company_docs', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.pad:
            pad_img = Image.open(self.pad.path)
            if pad_img.height > 1748 or pad_img.width > 1240:
                output_size = (1240, 1748)
                pad_img.thumbnail(output_size)
                pad_img.save(self.pad.path)

        if self.signature:
            signature_img = Image.open(self.signature.path)
            if signature_img.height > 118 or signature_img.width > 150:
                output_size = (150, 118)
                signature_img.thumbnail(output_size)
                signature_img.save(self.signature.path)