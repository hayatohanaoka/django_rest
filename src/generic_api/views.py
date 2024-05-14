from django.shortcuts import render
from django.contrib import auth
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView
)

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer, UserCreateSerializer, UserLoginSerializer
from .filters import CustomFilterBackend, PostFilter

# Create your views here.
class CommentRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

    def perform_update(self, serializer):
        comment = self.get_object()
        self._confirm_user(self.request, comment)
        serializer.save()
    
    def perform_destroy(self, instance):
        comment = self.get_object()
        self._confirm_user(self.request, comment)
        instance.delete()
    
    def _confirm_user(self, req, instance):
        if req.user.id != instance.author.id:
            raise PermissionError('User is not matched')


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'post_id'

    def get_queryset(self):
        if 'post_id' not in self.kwargs.keys():     
            post_id = self.kwargs['post_id']
            return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        kwarg_keys = self.kwargs.keys()
        if 'post_id' in kwarg_keys:
            post_id = self.kwargs['post_id']
            serializer.save(
                author=self.request.user,
                post_id=post_id
            )

"""
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


class PostListPagination(PageNumberPagination):
    page_size = 3                       # 1ページ当たりのデータ数の初期設定
    page_size_query_param = 'page_num'  # query e.g. /?page=1&page_num=6
    max_page_size = 10                  # 1ページに配置するデータの最大数
    last_page_strings = 'last'          # 最終ページのURLのクエリ文字列指定


class PostListLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 7


class PostCursorPagination(CursorPagination):
    ordering = '-id'


class PostApiView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    # カスタムバックエンドフィルターを使用
    filter_backends = (CustomFilterBackend,)

    # SearchFilter の使用
    # filter_backends = (SearchFilter,)
    # search_fields = (
    #     # 'title',
    #     'content',
    #     '$comments__comment'
    # )

    # 自分のカスタムフィルターを使う時の変数
    # filterset_class = PostFilter

    # django_filter を使用する際の変数
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('title','content', 'author')
    
    # pagination を使用する際の変数
    # pagination_class = PostListPagination
    # pagination_class = PostListLimitOffsetPagination
    # pagination_class = PostCursorPagination

    def get_queryset(self):
        return Post.objects.prefetch_related('comments').all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostApiFilterView(ListCreateAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # pagination_class = PostListPagination
    # pagination_class = PostListLimitOffsetPagination
    # pagination_class = PostCursorPagination

    def get_queryset(self):
        """
        自分でフィルターを定義する関数
        """
        if 'title' not in self.kwargs.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        posts = Post.objects.filter(title=self.kwargs['title'])
        return posts.prefetch_related('comments').all()

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
comment_retrieve_destroy_view = CommentRetrieveDestroyAPIView.as_view()
post_filter_view = PostApiFilterView.as_view()
