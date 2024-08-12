
from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.blog),
    path('temp/', views.temp),
    # path('register/', views.register, name='register')


]