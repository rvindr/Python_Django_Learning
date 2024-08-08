from django.shortcuts import render
from rest_framework.decorators import APIView
from account.serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status



class RegisterAPI(APIView):

    def post(self, request):
        data =request.data

        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'staus':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({
                'staus':True,
                'message':'user created successfully'
            }, status=status.HTTP_201_CREATED)
    

class LoginAPI(APIView):

    def post(self, request):

        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'message':serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(serializer.data)

            return Response(response, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'status':False,
                'message':'something went wrong',
                
            }, status=status.HTTP_400_BAD_REQUEST)
