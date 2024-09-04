from django.shortcuts import render
from home.tasks import add
from .scripts import scraper_imdb_news
from django.http import JsonResponse

# Create your views here.
def index(request):
    result = add.delay(10,5)
    return render(request, 'index.html',context={'data':'here is the demo text'})

def run_scraper(request):
    scraper_imdb_news()
    return JsonResponse({
        'status':True,
        'message':'scraper executed'
    })




