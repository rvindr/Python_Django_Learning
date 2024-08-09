import os
os.environ['DJANGO_SETTINGS_MODULE']='firstproject.settings'
import django
django.setup()
from home.models import Author, Book

# SubQuery in Django
from django.db.models import Subquery, OuterRef, Sum, Count


def handle():
    # 1. Latest Book for Each Author
    # book = Book.objects.filter(
    #     author_id = OuterRef('id')
    # ).order_by('-published_date').values('book_name')[:1]


    # authors = Author.objects.annotate(books = Subquery(book))

    # for author in authors:
    #     print(f'Author Name : {author.author_name} and Book Name : {author.books}')

    # 2. Total Price of Books Published in 2023 for Each Author
    # book = Book.objects.filter(
    #     author_id = OuterRef('id'),
    #     published_date__year = 2023 
    # ).values('author_id').annotate(total_price = Sum('price')).values('total_price')

    # authors = Author.objects.annotate(total_price_for_book =Subquery(book))

    # for author in authors:
    #     # print(vars(author))
    #     print(f'Author Name : {author.author_name} and Book  : {author.total_price_for_book}')

    # 3. Count of Books Published by Each Author
    book = Book.objects.filter(
        author_id = OuterRef('id')
    ).values('author_id').annotate(total_count = Count('id')).values('total_count')

    authors = Author.objects.annotate(book_count = Subquery(book))
    for author in authors:
        # print(vars(author))
        print(f'Author Name : {author.author_name} and Book  : {author.book_count}')


handle()



# 4. Average Price of Books for ach Author

# 5. Most Expensive Book for Each Author

# 6. Authors with at Least One Book Priced Over $50

# 7. Total Earnings for Each Author

# 8. Average Price of Books Published in 2023 for Each Author

# 9. Highest Priced Book for Each Author in 2023

# 10. Authors with Books Published in Each Month of 2023