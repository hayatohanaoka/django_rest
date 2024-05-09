from django.shortcuts import render
from django.contrib import auth
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer, UserCreateSerializer, UserLoginSerializer

# Create your views here.


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'post_id'

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(
            author=self.request.user,
            post_id=post_id
        )
"""
# 上のAPIViewを書き直すとこうなる？
class CommentListCreateAPIView(APIView):
    
    serializer_class = CommentSerializer
    model = Comment

    def get(self, req, *args, **kwargs):
        comments = self.model.objects.all()
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)
    
    def post(self, req, *args, **kwargs):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                author=req.user,
                post_id=kwargs['post_id']
            )
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
"""

class PostAPIDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'


class PostApiView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        posts = Post.objects.prefetch_related('comments').all()
        print(posts)
        return posts

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
post_detail_view = PostAPIDetailView.as_view()
comment_list_create_view = CommentListCreateAPIView.as_view()
