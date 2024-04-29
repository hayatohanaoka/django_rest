from django.contrib import auth
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import ItemModelSerializer, ProductModelSerializer, UserModelSerializer
from .permissions import CustomPermission
from second_rest_api.models import Item, Product

# Create your views here.
class BaseListView(APIView):
    """
    リソースの一覧取得と追加の処理を持ったベースView
    """
    # permission_classes = [
    #     # CustomPermission,
    #     # permissions.IsAdminUser,               # ログインしているかつ、管理者であればアクセス可
    #     # permissions.IsAuthenticated,           # ログインしていればアクセス可
    #     # permissions.IsAuthenticatedOrReadOnly, # ログイン済みもしくは、読み取り（GET）の場合はアクセス可
    #     # permissions.AllowAny                   # 誰でもアクセス可
    # ]
    def get(self, req, *arg, **kwarg):
        items = self.model.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)
    
    def post(self, req, *arg, **kwarg):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)


class BaseDetailView(APIView):
    """
    リソースの詳細の取得・消去・更新の処理を持ったベースView
    """

    def get(self, req, id):
        try:
            obj = self.model.objects.get(id=id)
        except:
            return Response(
                {'msg': f'primary key number {id} is not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(obj)
        return Response(serializer.data)
    
    def put(self, req, id):
        obj = self.model.objects.get(id=id)
        serializer = self.serializer_class(obj, data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    
    def delete(self, req, id):
        obj = self.model.objects.get(id=id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, req, id):
        obj = self.model.objects.get(id=id)
        serializer = self.serializer_class(obj, data=req.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class ItemModelView(BaseListView):

    model = Item
    serializer_class = ItemModelSerializer


class ProductModelView(BaseListView):
    
    serializer_class = ProductModelSerializer
    model = Product


class UserModelView(BaseListView):

    serializer_class = UserModelSerializer
    model = auth.get_user_model()


class ItemModelDetailView(BaseDetailView):

    model = Item
    serializer_class = ItemModelSerializer


class ProductModelDetailView(BaseDetailView):

    model = Product
    serializer_class = ProductModelSerializer


class UserModelDetailView(BaseDetailView):

    model = auth.get_user_model()
    serializer_class = UserModelSerializer


item_api = ItemModelView.as_view()
item_detail = ItemModelDetailView.as_view()

user_api = UserModelView.as_view()
user_detail = UserModelDetailView.as_view()

product_api = ProductModelView.as_view()
product_detail = ProductModelDetailView.as_view()
