
from django.urls import path
from account.views import UserRegisterView, UserLoginView, PrivateAPI

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('private/', PrivateAPI.as_view(), name='private')

]
