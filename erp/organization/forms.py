from django import forms
from django.forms import ModelForm
from .models import Organizations


class OrganizationsFrom(ModelForm):

    class Meta:
        model = Organizations
        fields = '__all__'