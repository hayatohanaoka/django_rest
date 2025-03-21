from django.urls import path, include

from . import views

urlpatterns = [
    path('posts/', views.post_api_views, name='posts'),
    path('post/<int:id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/comments/',
        views.comment_list_create_view, name='comments'),
    path('sign_up/', views.user_create_view, name='sign_up'),
    path('sign_in/', views.user_login_view, name='sign_in'),
]
