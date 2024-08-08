
from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'item'

urlpatterns = [
    path('', items, name='items'),
    path('<int:pk>', detail, name='detail'),
    path('add-items', add_items, name='add_items'),
    path('<int:pk>/delete-item/',delete_item, name='delete_item'),
    path('<int:pk>/edit-item/',edit, name='edit'),



]
