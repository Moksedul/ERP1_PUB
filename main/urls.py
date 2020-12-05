from django.urls import path

from core.views import load_person_image
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('settings', views.settings, name='main-settings'),
    path('load_person_image/', load_person_image, name='load-person-image'),
]
