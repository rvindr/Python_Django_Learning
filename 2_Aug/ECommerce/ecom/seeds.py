import os
import django
import random
from faker import Faker
from django.core.files import File
from django.contrib.auth.models import User
from items.models import Category, Item  # Replace 'items' with the actual name of your Django app

# Ensure the settings module is set up
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')  # Replace 'ecom' with your project name
django.setup()

fake = Faker()

def get_sample_image():
    """Returns a sample image file."""
    import requests
    from io import BytesIO

    url = 'https://picsum.photos/200/300'
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    return None

def create_fake_items(num_items_per_category=10):
    categories = Category.objects.all()
    for category in categories:
        for _ in range(num_items_per_category):
            name = fake.word().capitalize()
            description = fake.text()
            price = round(random.uniform(10.0, 1000.0), 2)
            is_sold = fake.boolean()
            created_by = User.objects.order_by('?').first()  # Assign a random user
            image_file = get_sample_image()

            item = Item(
                category=category,
                name=name,
                description=description,
                price=price,
                is_sold=is_sold,
                created_by=created_by,
                created_at=fake.date_this_year(),
            )

            if image_file:
                item.image.save(f"{name}.jpg", File(image_file), save=False)

            item.save()

if __name__ == "__main__":
    create_fake_items()
