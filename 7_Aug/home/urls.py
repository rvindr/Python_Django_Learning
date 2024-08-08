
from django.contrib import admin
from django.urls import path, include
from home.views import ProductDetailAPIView

urlpatterns = [
    path('product/', ProductDetailAPIView.as_view())
]
