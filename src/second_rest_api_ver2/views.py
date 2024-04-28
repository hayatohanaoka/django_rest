from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ItemModelSerializers
from second_rest_api.models import Item

# Create your views here.
class ItemModelView(APIView):
    """
    一覧の取得と新しいリソースの作成を行うView
    """

    serializer_class = ItemModelSerializers

    def get(self, req, *arg, **kwarg):
        items = Item.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)
    
    def post(self, req, *arg, **kwarg):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)


class ItemModelDetailView(APIView):
    """
    各リソースの詳細の取得と消去と更新を行うView
    """

    serializer_class = ItemModelSerializers

    def get(self, req, id):
        try:
            item = Item.objects.get(id=id)
        except:
            return Response(
                {'msg': f'primary key number {id} is not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(item)
        return Response(serializer.data)
    
    def put(self, req, id):
        item = Item.objects.get(id=id)
        serializer = self.serializer_class(item, data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    
    def delete(self, req, id):
        item = Item.objects.get(id=id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, req, id):
        item = Item.objects.get(id=id)
        serializer = self.serializer_class(item, data=req.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


api = ItemModelView.as_view()
detail = ItemModelDetailView.as_view()
