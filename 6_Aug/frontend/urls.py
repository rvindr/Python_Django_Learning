
from django.urls import path
from frontend import views
app_name = "frontend"

urlpatterns = [
    path('', views.blog, name="index"),
    path('login/', views.loginForm),
    path('client-blog/', views.client_blog),
    path('register/', views.registerForm, name='register')


]