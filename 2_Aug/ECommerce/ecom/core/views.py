from django.shortcuts import render, redirect
from items.models import *
from .forms import SignupForm

def index(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories
    }
    return render(request, 'core/index.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', context={'form': form})
