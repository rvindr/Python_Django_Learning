from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', index, name = 'index'),
    path('about/', about, name='about'),
    path('contact/',contact, name='contact'),
    path('signup/',signup, name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout')


]
