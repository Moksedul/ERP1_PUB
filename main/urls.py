from django.urls import path
from django.views.generic import TemplateView

from core.views import load_person_image
from core.test import convert_to_demo
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('settings', views.settings, name='main-settings'),
    path('load_person_image/', load_person_image, name='load-person-image'),
    path('loader/', TemplateView.as_view(template_name='main/loader.html')),
    path('convert_demo', convert_to_demo, name='convert-demo'),
]
