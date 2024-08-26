from django.shortcuts import render, redirect
from .models import Registration, LoginRequestModel
from .mongo_client import users_collection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bcrypt import hashpw, checkpw, gensalt
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed

class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            # Validate input data using the Pydantic model
            user_data = Registration(**request.data)

            # Check if the username or email already exists
            if users_collection.find_one({"username": user_data.username}):
                return Response({"error": "Username already exists"}, status=status.HTTP_409_CONFLICT)

            if users_collection.find_one({"email": user_data.email}):
                return Response({"error": "Email already exists"}, status=status.HTTP_409_CONFLICT)

            # Hash the password using bcrypt
            hashed_password = hashpw(user_data.password.encode('utf-8'), gensalt()).decode('utf-8')

            # Create a new user document
            user_document = {
                "username": user_data.username,
                "email": user_data.email,
                "password": hashed_password,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name
            }

            # Insert the user document into MongoDB
            users_collection.insert_one(user_document)

            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Format Pydantic validation errors
            errors = e.errors()
            formatted_errors = {
                "errors": [
                    {
                        "field": error['loc'][0],
                        "message": error['msg']
                    } for error in errors
                ]
            }
            return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)

        except DuplicateKeyError:
            return Response({"error": "Username or email already exists"}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"error": "An error occurred while creating the user"}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Validate the input data using Pydantic
            data = LoginRequestModel(**request.data)
            # print(request.data)
            # print(type(request.data))

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the user from MongoDB
        user = users_collection.find_one({"username": data.username})

        if not user or not checkpw(
            data.password.encode("utf-8"),
            user["password"].encode("utf-8")):

            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        # print(type(str(user["_id"])))
        # print(user["_id"])

        # generate JWT token
        payload = {
            'id' : str(user["_id"]),
            'exp' : datetime.utcnow() + timedelta(minutes = 1),
            'iat' : datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm = "HS256")
        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "message" : "login successfully",
            "jwt" : token
        }
        return response
    

class PrivateAPI(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            'message' : "you are authenticated"
        })

