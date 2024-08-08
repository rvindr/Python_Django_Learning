from django.shortcuts import render, get_object_or_404, redirect
from items.models import *
from .forms import AddItems, EditItemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def items(request):

    query = request.GET.get('query','')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    

    return render(request,'items/items.html' ,{
        'items':items,
        'query':query,
        'categories':categories,
        'category_id':int(category_id)
    })

def detail(request, pk):
    item = get_object_or_404(Item,pk=pk)
    related_items = Item.objects.filter(category = item.category, is_sold=False).exclude(pk=pk)
    return render(request, 'items/details.html', context={
        'item':item,
        'related_items':related_items
    })

@login_required
def add_items(request):
    if request.method == 'POST':

        form = AddItems(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = AddItems()
    
    return render(request, 'items/add_item.html', context={
        'form':form
    })

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user)
    item.delete()

    return redirect('dashboard:index')



@login_required
def edit(request, pk):
    print(request.method)
    item = get_object_or_404(Item,pk=pk, created_by= request.user)

    if request.method == 'POST':

        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    
        return render(request, 'items/add_item.html', context={
            'form':form
        })