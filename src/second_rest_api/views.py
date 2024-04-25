from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ItemSerializers

# Create your views here.
class ItemView(APIView):

    serializer_class = ItemSerializers

    def get(self, req, *arg, **kwarg):
        return Response({'method': 'get'})
    
    def post(self, req, *arg, **kwarg):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() # ItemSerializers の create が処理される
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)
    
    def put(self, req, *arg, **kwarg):
        return Response({'method': 'put'})

api = ItemView.as_view()
