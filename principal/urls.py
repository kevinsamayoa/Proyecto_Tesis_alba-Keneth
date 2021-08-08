from django.conf.urls import url
from django.urls import path

from .views import *

app_name = 'principal'

urlpatterns = [
    path('', home, name='home'),
]
