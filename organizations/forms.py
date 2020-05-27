from django import forms
from django.forms import ModelForm
from .models import Persons


class OrganizationsFrom(ModelForm):

    class Meta:
        model = Persons
        fields = '__all__'