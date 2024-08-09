# aggregator and annotation
import os
os.environ['DJANGO_SETTINGS_MODULE']='firstproject.settings'
import django
django.setup()
from home.models import Author, Book
from django.db.models import Avg, Sum, Min, Max, Count, Q


def handle():
    '''Aggregate '''
    # Total books
    books = Book.objects.all()
    print(f'Total Books {books.count()}')

    # Average book price
    book = Book.objects.aggregate(book_average = Avg('price'))
    print(f'Average book price {book}')

    # Total sum of  book price
    book = Book.objects.aggregate(book_total = Sum('price'))
    print(f'Total sum of  book price {book}')

    # Min price of book 
    book = Book.objects.aggregate(book_minimum = Min('price'))
    print(f'Min price of book {book}')

    # Max price of book 
    book = Book.objects.aggregate(book_maximum = Max('price'))
    print(f'Max price of book  {book}')


def ann_handle():
    # authors  = Author.objects.annotate(total_books = Count('book'),
    #                                    avg_price = Avg('book__price'),
    #                                    min_price = Min('book__price'),
    #                                    max_price = Max('book__price')
    #                                    )

    # for author in authors:
    #     print(f'Author name : {author.author_name} | Total Books : {author.total_books}')
    #     print(f'Book Avg price : {author.avg_price} | Min price : {author.min_price} | Max price : {author.max_price}')
    #     print('---------------------------')

    # authors = Author.objects.annotate(
    #     book_count= Count('book', filter=Q(book__published_date__year__gte = 2000)))
        
    # authors = Author.objects.annotate(
    #     book_count= Count('book', filter=Q(book__price__gte = 50))).filter(book_count__gte = 1)
    # for author in authors:
    #     print(f'Author name : {author.author_name} | Total Books : {author.book_count}')
        
            
    authors = Author.objects.annotate(
        earning = Sum('book__price')
        
        )
    for author in authors:
        print(f'Author name : {author.author_name} | Total Books : {author.earning}')

ann_handle()