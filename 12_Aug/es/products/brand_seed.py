# your_app/management/commands/seed_brands.py
from .models import Brand

def handle( *args, **kwargs):
        brands = ['Apple', 'Samsung', 'Sony', 'Nike', 'Adidas', 'Micromax', 'JBL']

        for brand_name in brands:
            Brand.objects.create(brand_name=brand_name)

       
