from django.urls import path
from . import views 

urlpatterns = [
    path('', views.api, name='index_model'),
    path('<int:id>/', views.detail, name='detail_model')
]