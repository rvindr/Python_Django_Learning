

from django.urls import path, include
from home.views import PersonAPI, RegisterAPI, LoginAPI

urlpatterns = [
    path('person/',PersonAPI.as_view()),
    path('register/',RegisterAPI.as_view()),
    path('login/',LoginAPI.as_view())



]
