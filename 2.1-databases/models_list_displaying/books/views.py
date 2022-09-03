from django.shortcuts import render
from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(request, template, context)


def books_view_detail(request, detail_date):
    template = 'books/books_detail.html'
    books = Book.objects.filter(pub_date_str=detail_date)
    previous_page = Book.objects.filter(pub_date_str__lt=detail_date).order_by('-pub_date_str').first()
    next_page = Book.objects.filter(pub_date_str__gt=detail_date).order_by('pub_date_str').first()
    context = {
        'books': books,
        'previous_page': previous_page,
        'next_page': next_page,
    }
    return render(request, template, context)