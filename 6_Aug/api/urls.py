
from django.urls import path
from account.views import RegisterAPI, LoginAPI
from blog.views import BlogAPI, PublicView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
urlpatterns += [

    path('register/', RegisterAPI.as_view() ),
    path('login/', LoginAPI.as_view() ),
    path('blog-post/', BlogAPI.as_view() ),
    path('blogs/', PublicView.as_view() )



]
