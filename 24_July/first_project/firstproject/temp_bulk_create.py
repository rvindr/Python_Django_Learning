import os
os.environ['DJANGO_SETTINGS_MODULE']='firstproject.settings'
import django
django.setup()
from home.models import *
from faker import Faker
import time
fake = Faker('en-IN')

def create(number):
    # Given below is not a right way to create bulk data-it's time taken
    # for i in range(number):
    #     Person.objects.create(person_name = fake.name())

    create = []
    for _ in range(number):
        create.append(Person(person_name = fake.name()))
    Person.objects.bulk_create(create)

def update_person(name):
    print(Person.objects.filter(person_name__icontains =name).count())
    print(Person.objects.filter(person_name__icontains =name).update(person_name = 'Ravinder'))



def bulk_delete():
    Person.objects.all().delete()

# start = time.perf_counter()
# create(10000)
# end = time.perf_counter()
# print(f'Time taken : {end-start}')
# bulk_delete()

update_person('Saini')