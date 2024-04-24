from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timezone
import pytz
from pytz.exceptions import UnknownTimeZoneError

# Create your views here.
class IndexView(View):
    def get(self, req, *arg, **kwarg):
        # return JsonResponse({'page': 'hello!!'})
        return HttpResponse('<h1>Hello!</h1>')

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def country_datetime(req):
    try:
        if req.method == 'POST':
            if 'timezone' in req.data.keys():        
                requested_timezone = req.data['timezone']
                tz = pytz.timezone(requested_timezone)    # reqのタイムゾーン
                utc_datetime = datetime.now(timezone.utc) # UTC
                return Response(
                    {f'Datetime POST: {requested_timezone}': utc_datetime.astimezone(tz)}
                )
        elif req.method == 'PUT':
            print('PUTメソッドで送信')
        elif req.method == 'DELETE':
            print('DELETEメソッドで送信')
        else:
            if 'timezone' in req.GET.keys():
                requested_timezone = req.GET['timezone']
                tz = pytz.timezone(requested_timezone)
                utc_datetime = datetime.now(timezone.utc)
                return Response({f'Datetime GET: {requested_timezone}': utc_datetime.astimezone(tz)})
        return Response({'Datetime': datetime.now()})
    except UnknownTimeZoneError as e:
        return Response({'Error request': 'Unknown timezone error'}, status=status.HTTP_400_BAD_REQUEST)

index = IndexView.as_view()
