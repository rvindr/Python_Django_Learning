
from django.urls import path
from account.views import RegisterAPI, LoginAPI
from blog.views import BlogAPI, PublicView

urlpatterns = [

    path('register/', RegisterAPI.as_view() ),
    path('login/', LoginAPI.as_view() ),
    path('blog-post/', BlogAPI.as_view() ),
    path('blogs/', PublicView.as_view() )



]
