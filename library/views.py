from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book, Person, BookLoan
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookForm, PersonForm, BookLoanForm
from django.utils import timezone

@login_required
def view_books(request):
    query = request.GET.get('search', '')
    if query:
        books = Book.objects.filter(
            title__icontains=query, library=request.user.library
        ).union(
            Book.objects.filter(author__icontains=query, library=request.user.library)
        ).order_by('title') 
    else:
        books = Book.objects.filter(library=request.user.library).order_by('title')

    paginator = Paginator(books, 30) 
    page = request.GET.get('page')

    try:
        book_paginated = paginator.page(page)
    except PageNotAnInteger:
        book_paginated = paginator.page(1)
    except EmptyPage:
        book_paginated = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = BookForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro criado com sucesso!')
            return redirect('library:view_books')
        else:
            messages.error(request,"Erro ao criar livro. Verifique os dados e tente novamente.")
    else:
        form = BookForm(user=request.user)

    context={
        'books': book_paginated, 
        'query': query, 
        'form': form
    }

    return render(request, 'library/Book/view_books.html', context)

@login_required
def details_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro editado com sucesso!')
            return redirect('library:details_book', book_id=book_id)
        else:
            messages.error(request, 'Error ao tentar editar o livro. Verifique os dados e tente novamente.')
    else:
        form = BookForm(instance=book, user=request.user)

    context={
        'book': book, 
        'form': form
    }
    return render(request, 'library/Book/details_book.html', context)

@login_required
def view_peoples(request):
    if not request.user.library:
        messages.warning(request, "Você precisa estar associado a uma biblioteca para ver as pessoas.")
        people = Person.objects.none()
        form = PersonForm(user=request.user)
        return render(request, 'library/people/people_list.html', context={'peoples': people, 'form': form})
    
    query = request.GET.get('search', '')
    if query:
        people = Person.objects.filter(name__icontains=query, library=request.user.library).order_by('name')
    else:
        people = Person.objects.filter(library=request.user.library).order_by('name')

    paginator = Paginator(people, 30) 
    page = request.GET.get('page')

    try:
        people_paginated = paginator.page(page)
    except PageNotAnInteger:
        people_paginated = paginator.page(1)
    except EmptyPage:
        people_paginated = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = PersonForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Pessoa criada com sucesso!")
            return redirect('library:view_peoples')
    else:
        form = PersonForm(user=request.user)

    context={
        'peoples': people_paginated, 
        'query': query,
        'form': form
    }
    return render(request, 'library/Person/view_people.html', context)

@login_required
def details_people(request, person_id):
    person = get_object_or_404(Person, id=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pessoa editada com sucesso!')
            return redirect('library:details_people', person_id=person_id)
        else:
            messages.error(request, 'Error ao tentar editar a pessoa. Verifique os dados e tente novamente.')
    else:
        form = PersonForm(instance=person, user=request.user)

    context={
        'person': person, 
        'form': form
    }

    return render(request, 'library/Person/details_people.html', context)

@login_required
def view_loans(request):
    if not request.user.library:
        messages.warning(request, "Você precisa estar associado a uma biblioteca para ver os empréstimos.")
        loans = BookLoan.objects.none()
        form = BookLoanForm(user=request.user)
        return render(request, 'library/loan/view_loans.html', context={'loans': loans, 'form': form})

    query = request.GET.get('search', '')
    if query:
        loan = BookLoan.objects.filter(
            Q(books__title__icontains=query)   | Q(books__author__icontains=query) |
            Q(person__name__icontains=query),
            library=request.user.library
        ).order_by('loan_date')
    else:
        loan = BookLoan.objects.filter(library=request.user.library).order_by('loan_date')

    paginator = Paginator(loan, 30) 
    page = request.GET.get('page')

    try:
        loan_paginated = paginator.page(page)
    except PageNotAnInteger:
        loan_paginated = paginator.page(1)
    except EmptyPage:
        loan_paginated = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = BookLoanForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Empréstimo criado com sucesso!")
            return redirect('library:view_loans')
        else:
            messages.error(request, "Erro ao criar empréstimo. Verifique os dados e tente novamente.")
    else:
        form = BookLoanForm(user=request.user)

    context={
        'loans': loan_paginated,
        'query': query, 
        'form': form
    }

    return render(request, 'library/BookLoan/view_loans.html', context)

@login_required
def details_loan(request, loan_id):
    loan = get_object_or_404(BookLoan, id=loan_id)
    
    if request.method == 'POST':
        form = BookLoanForm(request.POST, instance=loan, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Empréstimo atualizado com sucesso!")
            return redirect('library:details_loan', loan_id=loan.id)
        else:
            messages.error(request, "Erro ao atualizar empréstimo. Verifique os dados e tente novamente.")
    else:
        form = BookLoanForm(instance=loan, user=request.user)

    context={
        'loan': loan, 
        'form': form
    }

    return render(request, 'library/BookLoan/details_loan.html', context)

@login_required
def returned_loan(request, loan_id):
    loan = get_object_or_404(BookLoan, id=loan_id)

    if request.method == 'POST':
        loan.status = BookLoan.StatusLoan.RETURNED
        loan.return_date = timezone.now()
        loan.books.update(status=Book.StatusBook.AVAILABLE)
        if not loan.date_previous_return:
            loan.date_previous_return = timezone.now()
        loan.save()
        messages.success(request, "Empréstimo devolvido com sucesso!")
        return redirect('library:view_loans')
    else:
        messages.error(request, "Erro ao devolver o empréstimo. Tente novamente.")
    return redirect('library:details_loan', loan_id=loan_id) 

@login_required
def pickup_loan(request, loan_id):
    loan = get_object_or_404(BookLoan, id=loan_id)

    if request.method == 'POST':
        loan.status = BookLoan.StatusLoan.ACTIVE
        loan.books.update(status=Book.StatusBook.CHECKED_OUT)
        loan.loan_date = timezone.now()
        loan.save()
        messages.success(request, 'Reserva alterada para Empréstimo com sucesso!')
        return redirect('library:view_loans')
    else:
        messages.error(request, 'Error ao tentar retirar reserva do emprestimo. Tente novamente.')
    return redirect('library:details_loan', loan_id=loan_id)

@login_required
def cancel_loan(request, loan_id):
    loan = get_object_or_404(BookLoan, id=loan_id)

    if request.method == 'POST':
        loan.status = BookLoan.StatusLoan.CANCELLED
        loan.books.update(status=Book.StatusBook.AVAILABLE)
        loan.save()
        messages.success(request, "Empréstimo cancelado com sucesso!")
        return redirect('library:view_loans')
    else:
        messages.error(request, "Erro ao cancelar o empréstimo. Tente novamente.")
    
    return redirect('library:details_loan', loan_id=loan_id)
    