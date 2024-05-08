from django.shortcuts import render
from django.contrib import auth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView
)

from .models import Post
from .serializers import PostSerializer, UserCreateSerializer, UserLoginSerializer
# Create your views here.


class PostApiView( ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserCreateView(CreateAPIView):
    model = auth.get_user_model()
    serializer_class = UserCreateSerializer


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, req):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            user = auth.authenticate(
                request=req,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            auth.login(request=req, user=user)
            return Response('ログイン成功', status=status.HTTP_202_ACCEPTED)
        return Response('ログイン失敗', status=status.HTTP_401_UNAUTHORIZED)

post_api_views = PostApiView.as_view()
user_create_view = UserCreateView.as_view()
user_login_view = UserLoginAPIView.as_view()
