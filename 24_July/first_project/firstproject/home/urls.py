from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('contact', contact),
    path('dynamic_route/<number>/', dynamic_route),
    path('search/', search_page)
]
