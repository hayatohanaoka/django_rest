from django.urls import path
from . import views 

urlpatterns = [
    path('item/', views.item_api, name='item_index'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('user/', views.user_api, name='user_index'),
    path('user/<int:id>/', views.user_detail, name='user_detail'),
    path('product/', views.product_api, name='product_index'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
