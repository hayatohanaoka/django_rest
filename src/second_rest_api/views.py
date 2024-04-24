from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class ItemView(APIView):
    def get(self, req, *arg, **kwarg):
        return Response({'method': 'get'})
    
    def post(self, req, *arg, **kwarg):
        return Response({'method': 'post'})
    
    # def delete(self, req, *arg, **kwarg):
    #     return Response({'method': 'delete'})
    
    def put(self, req, *arg, **kwarg):
        return Response({'method': 'put'})

api = ItemView.as_view()
