
from django.contrib import admin
from django.urls import path
from scraper.views import index, scraper_imdb_news
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('run', scraper_imdb_news)
]
