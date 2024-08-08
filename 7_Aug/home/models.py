from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)
    price = models.FloatField()

    @property
    def sale_price(self):
        return self.price*0.8
    
    def __str__(self) -> str:
        return self.name