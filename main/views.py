from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from orders.models import Orders


# Create your views here.
@login_required()
def home(request):
    order_count = Orders.objects.all().count()
    context = {
        'order_count': order_count
    }
    return render(request, 'main/home.html', context)


@login_required()
def settings(request):
    return render(request, 'main/settings_home.html')

