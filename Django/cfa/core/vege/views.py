from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def receipes(request):
    if request.method == "POST":
        data = request.POST

        recipe_name = data.get('recipe_name')
        recipe_desc = data.get('recipe_desc')
        recipe_img = request.FILES.get('recipe_img')

        Recipe.objects.create(recipe_name=recipe_name,recipe_desc=recipe_desc,recipe_img=recipe_img)

        return redirect('/receipes')
    
    context = {
        'receipes_data' : Recipe.objects.all()
    }
    return render(request, 'vege/receipes.html',context)

def delete_receipe(request, id):

    queryset = Recipe.objects.get(id=id)
    queryset.delete()

    return redirect('/receipes/')

def update_receipe(request, id):

    queryset = Recipe.objects.get(id=id)
    context = {
        'receipe': queryset
    }

    if request.method == 'POST':
        data = request.POST

        recipe_name = data.get('recipe_name')
        recipe_desc = data.get('recipe_desc')
        recipe_img = request.FILES.get('recipe_img')

        queryset.recipe_name = recipe_name
        queryset.recipe_desc = recipe_desc
        if recipe_img:
            queryset.recipe_img = recipe_img

        queryset.save()
        return redirect('/receipes/')

    return render(request, 'vege/update.html', context)