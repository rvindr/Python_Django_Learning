from django.shortcuts import render
from rest_framework.decorators import APIView
from home.models import Person
from home.serializers import PersonSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator

# Create your views here.


class PersonAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        persons = Person.objects.all()
        #paginaiton
        try:
            page = request.GET.get('page',1)
            page_size = 3
            paginator = Paginator(persons, page_size)
            print(paginator.page(page))
            serializer = PersonSerializer(paginator.page(page), many=True)
        except Exception as e:
            return Response({
                'status':False,
                'message':'Invalid page number'
            })



        # serializer = PersonSerializer(persons, many=True)

        return Response({
            'status':True,
            'data':serializer.data
        })
    
    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status':True,
                'message':'Data added in database',
                'data' : serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
                'status':False,
                'message':'Something went wrong',
                'data' : serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors,

            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
                'status':True,
                'message':'user created',
                'data':serializer.data
            }, status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status':False,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])

        if not user:
            return Response({
                'status':False,
                'message':"invalid credential",
            }, status=status.HTTP_400_BAD_REQUEST)
        token,_ = Token.objects.get_or_create(user=user)
        return Response({
            'status':True,
            'message':'user login',
            'token':str(token)
        }, status=status.HTTP_202_ACCEPTED)