from django.conf.urls import url
from django.urls import path

from .views import *

app_name = 'principal'

"""Urls disponibles en el la aplicación"""

urlpatterns = [
    path('', home, name='home'),
    path('mapa', mapa, name='mapa'),
    path('dashboard', dashboard, name='dashboard'),
    path('manual', manual, name='manual'),
]
