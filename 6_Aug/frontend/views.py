from django.shortcuts import render


def blog(request):
    return render(request, 'frontend/index.html')


def temp(request):
    return render(request, 'frontend/temp.html')