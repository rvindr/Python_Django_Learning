from django.shortcuts import render


def blog(request):
    return render(request, 'frontend/index.html')


def loginForm(request):
    return render(request, 'frontend/login.html')

def registerForm(request):
    return render(request, 'frontend/register.html')

def client_blog(request):
    return render(request, 'frontend/client_blog.html')