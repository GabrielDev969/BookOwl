from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book, Person, BookLoan
from django.contrib import messages
from .forms import BookForm, PersonForm, BookLoanForm

def view_books(request):
    query = request.GET.get('search', '')
    if query:
        books = Book.objects.filter(title__icontains=query)  | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()

    paginator = Paginator(books, 25) 
    page = request.GET.get('page')

    try:
        book_paginated = paginator.page(page)
    except PageNotAnInteger:
        book_paginated = paginator.page(1)
    except EmptyPage:
        book_paginated = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro criado com sucesso!")
            return redirect('library:view_books')
        else:
            messages.error("Erro ao criar livro. Verifique os dados e tente novamente.")
    else:
        form = BookForm()
    return render(request, 'library/Book/view_books.html', context={'books': book_paginated, 'query': query, 'form': form})

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