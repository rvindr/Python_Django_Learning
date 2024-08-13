from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Registration
from .mongo_client import users_collection
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

class UserCreateView(APIView):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name")
        }

        try:
            # Validate data using Pydantic
            user_data = Registration(**data)
            
            # Check if user already exists
            if users_collection.find_one({'username': user_data.username}) or \
               users_collection.find_one({'email': user_data.email}):
                messages.error(request, 'User already exists')
                return redirect('user-register')
            
            # Hash the password
            hashed_password = make_password(user_data.password)
            
            # Create user in MongoDB
            user_document = {
                'username': user_data.username,
                'email': user_data.email,
                'password': hashed_password,
                'first_name': user_data.first_name,
                'last_name': user_data.last_name
            }
            users_collection.insert_one(user_document)
            messages.success(request, 'User created successfully')
            return redirect('user-register')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('user-register')