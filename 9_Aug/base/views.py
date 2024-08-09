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


def login(request):

    if request.method == "POST":

        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            data = {
                 "username" : username,
                 "password" : password
            }
            print(data)

            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                    print('inside the not valid')
                    res = Response({
                        'status':False,
                        'message':serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)

                    return render(request, 'login.html', context={
                         'data' :res
                    })


            response = serializer.get_jwt_token(serializer.data)

            return render(request, 'login.html', context={
                            'data' :response
                        })
        except Exception as e:
                res =  Response({
                    'status':False,
                    'message':'something went wrong',
                    
                }, status=status.HTTP_400_BAD_REQUEST)
                return render(request, 'login.html', context={
                         'data' :res
                    })
        
    return render(request, 'login.html')
        