
from django.contrib import admin
from django.urls import path
from home.views import index, run_scraper

urlpatterns = [
    path('',index),
    path('run-scraper/',run_scraper),
    path('admin/', admin.site.urls),
]
