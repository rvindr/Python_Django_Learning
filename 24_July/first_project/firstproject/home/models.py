from typing import Iterable
from django.db import models
from home.utils import generate_slug



class College(models.Model):
    college_name = models.CharField(max_length=100)
    college_address = models.CharField(max_length=100)
    def __str__(self): return self.college_name




class Student(models.Model):
    gender_choices = (('M','Male'),('F','Female'))
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True)
    name =models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=gender_choices, default='Male')
    age = models.IntegerField(null=True, blank=True)
    # date_of_birth = models.DateField()
    # profile_img = models.ImageField(null=True, blank=True, upload_to='student/profile_img')
    # file = models.FileField(null=True, blank=True, upload_to='student/file')
    # created_at = models.DateTimeField(auto_created=True)
    # updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    author_name = models.CharField(max_length=100)

    def __str__(self):return self.author_name

class Book(models.Model):
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    book_name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    def __str__(self):return self.book_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    country = models.CharField(default='IN', max_length=100)
    def __str__(self): return self.brand_name


class Products(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.slug = generate_slug(self.product_name, Products)

        return super().save(*args, **kwargs)

    def __str__(self): return self.product_name

class Skills(models.Model):
    skill_name = models.CharField(max_length=100)
    def __str__(self): return self.skill_name


class Person(models.Model):
    person_name = models.CharField(max_length=100)
    skill = models.ManyToManyField(Skills)
    def __str__(self): return self.person_name

class StudentData(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    dob = models.DateField()
    father_name = models.CharField(max_length=100)

    def __str__(self): return self.name
