from typing import Any
from django.http import HttpResponseForbidden
from home.models import Store
ALLOWED_IP = ['123.45.69.89','987.65.456.20']
class IPBlocking:

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        print(ip)
        if ip in ALLOWED_IP:
            return HttpResponseForbidden("Forbidden : IP not allowd")
        
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

class CheckBMPHeader:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        headers = request.headers

        if 'bmp' not in headers:
            return HttpResponseForbidden('Missing : Header *bmp*')
        else:
            if not Store.objects.filter(bmp_id = headers.get('bmp')).exists():
                return HttpResponseForbidden('Wrong bmp id')
        return self.get_response(request)