from django.shortcuts import render
from django.http import JsonResponse
from .models import Store

def index(request):
    
    store = Store.objects.get(bmp_id = request.headers.get('bmp'))
    data = {
        'status':True,
        'message':'store data',
        'bmd_id' : store.bmp_id,
        'store_name': store.store_name
    }
    return JsonResponse(data)