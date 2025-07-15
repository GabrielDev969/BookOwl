from django.shortcuts import render, get_object_or_404
from .models import Book

def view_books(request):
    books = Book.objects.all()
    return render(request, 'library/Book/view_books.html', context={'books': books})

def details_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library/Book/details_book.html', context={'book': book})