import os
import django
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elasticproject.settings')
django.setup()

from products.models import Brand, Product

fake = Faker()

def seed_brands(num):
    """Seed the Brand model with fake data."""
    brands = []
    for _ in range(num):
        brand_name = fake.company()
        brand = Brand(brand_name=brand_name)
        brands.append(brand)
    Brand.objects.bulk_create(brands)
    print(f"{num} brands created.")

def seed_products(num):
    """Seed the Product model with fake data."""
    brands = list(Brand.objects.all())
    products = []
    for _ in range(num):
        title = fake.word()
        description = fake.text()
        category = fake.word()
        price = fake.random_number(digits=3) + fake.random_number(digits=2) / 100
        brand = fake.random_element(elements=brands) if brands else None
        sku = fake.unique.word()
        thumbnail = fake.image_url()
        product = Product(
            title=title,
            description=description,
            category=category,
            price=price,
            brand=brand,
            sku=sku,
            thumbnail=thumbnail
        )
        products.append(product)
    Product.objects.bulk_create(products)
    print(f"{num} products created.")

if __name__ == "__main__":
    seed_brands(10)  # Change this number if you want more or fewer brands
    seed_products(20)  # Change this number if you want more or fewer products
