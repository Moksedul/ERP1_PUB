from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def home(request):
    return render(request, 'main/home.html')


@login_required()
def settings(request):
    return render(request, 'main/settings_home.html')
