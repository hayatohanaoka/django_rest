from django.urls import path
from .views import index, country_datetime

urlpatterns = [
    path('', index, name='index'),
    path('datetime/', country_datetime, name='datetime')
]