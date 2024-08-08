
from django.contrib import admin
from django.urls import path, include
# from home.views import ProductDetailAPIView
from home.views import ProductAPI


urlpatterns = [
    path('product/', ProductAPI.as_view()),


]
