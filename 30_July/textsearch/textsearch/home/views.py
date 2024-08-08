from django.shortcuts import render
from .models import Product, Tags

def search_products(request):
    search_query = request.GET.get('search', '')
    brand_query = request.GET.get('brand', '')
    category_query = request.GET.get('category', '')
    min_price_query = request.GET.get('min_price', '0')
    max_price_query = request.GET.get('max_price', '1000')

    products = Product.objects.all()

    if search_query:
        products = products.filter(title__icontains=search_query)
    
    if brand_query:
        products = products.filter(brand=brand_query)
    
    if category_query:
        products = products.filter(category=category_query)
    
    if min_price_query and max_price_query:
        products = products.filter(price__gte=min_price_query, price__lte=max_price_query)

    brands = Product.objects.values('brand').distinct()
    categories = Product.objects.values('category').distinct()

    context = {
        'results': products,
        'search': search_query,
        'brands': brands,
        'categories': categories
    }

    return render(request, 'index.html', context)
