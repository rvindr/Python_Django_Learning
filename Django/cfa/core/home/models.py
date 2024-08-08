from django.db import models

class Student(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Car(models.Model):
    car_name = models.CharField(max_length=500)
    speed = models.IntegerField(default=50)

    def __str__(self):
        return self.car_name
