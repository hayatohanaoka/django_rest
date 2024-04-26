from django.urls import path
from . import views 

urlpatterns = [
    path('', views.api, name='index'),
    path('<int:id>/', views.detail, name='detail')
]