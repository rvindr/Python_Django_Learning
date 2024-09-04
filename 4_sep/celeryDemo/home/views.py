from django.shortcuts import render
from home.tasks import add

# Create your views here.
def index(request):
    result = add.delay(10,5)
    return render(request, 'index.html',context={'data':'here is the demo text'})