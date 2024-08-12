from django.db import models
import uuid

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=80)
    def __str__(self): return self.brand_name

class Products(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/products')
    category = models.CharField( max_length=50, choices=(
        ('Electonics','Electronics'),
        ('Mobiles','Mobiles'),
        ('Computer','Computer'),
        ('Clothes','Clothes'),
        ('Toys','Toys'),
        ('Grocery','Grocery')
    ))
    description = models.TextField()
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)
    def __str__(self): return self.title