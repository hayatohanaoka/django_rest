from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View

# Create your views here.
class IndexView(View):
    def get(self, req, *arg, **kwarg):
        # return JsonResponse({'page': 'hello!!'})
        return HttpResponse('<h1>Hello!</h1>')

index = IndexView.as_view()
