from home.models import *
from faker import Faker
fake = Faker('en-IN')
import random

def seed(records=10):
    # --------Use to create fake student data------------

    # college_names = ['JIET', 'LPU', 'PIET', 'CDLU', 'JCD', 'MDU', 'GJU', 'GEETA UNIVERSITY', 'KUK']

    # for name in college_names:
    #     address = fake.address()

    #     college.objects.create(
    #         college_name = name,
    #         college_address = address
    #     )

    # for i in range(records):
    #     college = College.objects.all()
    #     college_index = random.randint(0,college.count()-1)
    #     gender_choices = random.choice(['M','F'])
    #     college = college[college_index]
    #     name = fake.name()
    #     mobile_number = fake.phone_number()
    #     email = fake.email()
    #     gender = gender_choices
    #     age = random.randint(18,30)
    
    #     Student.objects.create(
    #         college = college,
    #         name = name,
    #         mobile_number = mobile_number,
    #         email = email,
    #         gender = gender,
    #         age = age)

    # --------Use to create fake author data------------

    # for i in range(records):
    #     Author.objects.create(
    #         author_name = fake.name()
    #     )
    # --------Use to create fake book data------------
    for i in range(records):
        author = Author.objects.all()
        author_index = random.randint(0, author.count()-1)

        author_id = author[author_index]
        book_name = fake.text(max_nb_chars = 20)
        price = round(random.uniform(10, 99), 2)
        published_date = fake.date()

        Book.objects.create(
            author_id=author_id,
            book_name=book_name,
            price=price,
            published_date=published_date
        )
