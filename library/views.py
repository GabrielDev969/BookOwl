from django.shortcuts import render, get_object_or_404
from .models import Book, Person, BookLoan

def view_books(request):
    books = Book.objects.all()
    return render(request, 'library/Book/view_books.html', context={'books': books})

def details_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library/Book/details_book.html', context={'book': book})

def view_peoples(request):
    peoples = Person.objects.all()
    return render(request, 'library/Person/view_people.html', context={'peoples': peoples})

def details_people(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    return render(request, 'library/Person/details_people.html', context={'person': person})

def view_loans(request):
    loans = BookLoan.objects.all()
    return render(request, 'library/BookLoan/view_loans.html', context={'loans': loans})

def details_loan(request, loan_id):
    loan = get_object_or_404(BookLoan, id=loan_id)
    return render(request, 'library/BookLoan/details_loan.html', context={'loan': loan})