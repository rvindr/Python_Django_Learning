from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import APIView
from base.api.serializers import  LoginSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@login_required(login_url="/login/")
def home(request):
    return render(request, 'home.html')




class LoginAPI():

    def __init__(self, data) -> None:
        self.data = data

    def post(self):

        try:

            serializer = LoginSerializer(data=self.data)

            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'message':serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(serializer.data)

            return response
        
        except Exception as e:
            return Response({
                'status':False,
                'message':'something went wrong',
                
            }, status=status.HTTP_400_BAD_REQUEST)
        
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {
                 "username" : username,
                 "password" : password
            }
        
        res = LoginAPI(data)
    
        return render(request, 'login.html',context={
            'data':res.post()
        })

    return render(request, 'login.html')
