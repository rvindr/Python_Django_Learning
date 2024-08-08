from django.db import models

# Create your models here.
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    about = models.TextField()
    company_type = models.CharField(max_length=100, choices=(
        ('IT','IT'),
        ('NON-IT','NON-IT'),
        ('MOBILES','MOBILES')))
    
    added = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.TextField()
    phone_num = models.CharField(max_length=12)
    about = models.TextField()
    position = models.CharField(max_length=50, choices=(
       ('Java Developer','JD'),
       ('Python Developer','PD'),
       ('Data Analyst','DA'),
       ('Data Scientist','DS')
    ))
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name