from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book, Person, BookLoan
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookForm, PersonForm, BookLoanForm
from django.utils import timezone
from django.core.files.storage import default_storage
from django.urls import reverse
import json
from django.http import JsonResponse
from .utils.import_books import validate_books, save_books 
import os

@login_required
def view_books(request):
    """
    View para listar livros, buscar, criar novos livros e importar arquivos.
    Exibe todos os livros quando nenhum filtro de status é aplicado.
    """
    # Busca e paginação
    query = request.GET.get('search', '')
    status_filters = request.GET.getlist('status')

    books = Book.objects.filter(library=request.user.library)
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    
    # Verfica os filtros
    if status_filters and status_filters != ['']:
        books = books.filter(status__in=status_filters)
    else:
        status_filters = [status[0] for status in Book._meta.get_field('status').choices]

    books = books.order_by('title')

    paginator = Paginator(books, 30)
    page = request.GET.get('page')
    try:
        book_paginated = paginator.page(page)
    except PageNotAnInteger:
        book_paginated = paginator.page(1)
    except EmptyPage:
        book_paginated = paginator.page(paginator.num_pages)

    # Inicializa o formulário de criação de livro
    form = BookForm(user=request.user)
    book_status_choices = Book._meta.get_field('status').choices

    context = {
        'books': book_paginated,
        'query': query,
        'form': form,
        'data_for_review': [],
        'has_errors': False,
        'selected_statuses': status_filters,
        'book_status_choices': book_status_choices,
    }

    if request.method == 'POST':
        # Verifica se é criação de livro
        if 'title' in request.POST:
            form = BookForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Livro criado com sucesso!')
                return redirect('library:view_books')
            else:
                messages.error(request, "Erro ao criar livro. Verifique os dados e tente novamente.")
                context['form'] = form

        # Verifica se é upload de arquivo
        elif 'file' in request.FILES:
            file = request.FILES['file']
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            
            # Cria o diretório temp/ se não existir
            try:
                os.makedirs(temp_dir, exist_ok=True)
            except Exception as e:
                messages.error(request, f"Erro ao criar diretório temporário: {str(e)}")
                return redirect('library:view_books')

            # Salva o arquivo no diretório temp/
            file_path = default_storage.save(f'temp/{file.name}', file)
            full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            file_type = 'xlsx' if file.name.endswith('.xlsx') else 'csv'

            # Valida o arquivo
            try:
                result = validate_books(full_file_path, file_type, user=request.user)
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {str(e)}")
                default_storage.delete(file_path)
                return redirect('library:view_books')

            # Remove o arquivo temporário
            default_storage.delete(file_path)

            if result['status'] == 'error':
                messages.error(request, 'Erro ao processar o arquivo: ' + ', '.join(result['errors']))
                return redirect('library:view_books')

            # Armazena os dados validados na sessão para confirmação
            request.session['books_for_review'] = json.dumps({
                'valid_books': [
                    {
                        'library_id': book.library_id,
                        'title': book.title,
                        'author': book.author,
                        'description': book.description,
                        'status': book.status
                    } for book in result['valid_books']
                ],
                'data_for_review': result['data_for_review'],
                'errors': result['errors']
            })

            # Adiciona dados de revisão ao contexto para exibir a modal
            context['data_for_review'] = result['data_for_review']
            context['has_errors'] = len(result['errors']) > 0

    return render(request, 'library/Book/view_books.html', context)

@login_required
def confirm_import(request):
    """
    View para confirmar a importação dos livros.
    """
    if request.method != 'POST':
        messages.error(request, 'Método inválido.')
        return redirect('library:view_books')

    books_data = request.session.get('books_for_review')
    if not books_data:
        messages.error(request, 'Nenhum dado para importar.')
        return redirect('library:view_books')

    books_data = json.loads(books_data)
    if books_data['errors']:
        messages.error(request, 'Não é possível importar com erros nos dados.')
        return redirect('library:view_books')

    # Reconstroi os objetos Book
    valid_books = [
        Book(
            library_id=book['library_id'],
            title=book['title'],
            author=book['author'],
            description=book['description'],
            status=book['status']
        ) for book in books_data['valid_books']
    ]

    # Salva os livros
    result = save_books(valid_books, batch_size=1000)

    if result['status'] == 'success':
        messages.success(request, f'{result["total_imported"]} livros importados com sucesso!')
        del request.session['books_for_review']
    else:
        messages.error(request, 'Erro ao importar livros: ' + ', '.join(result['errors']))

    return redirect('library:view_books')

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
    """
    View para listar empréstimos, buscar e criar novos empréstimos.
    Exibe todos os empréstimos quando nenhum filtro de status é aplicado.
    """
    if not request.user.library:
        messages.warning(request, "Você precisa estar associado a uma biblioteca para ver os empréstimos.")
        loans = BookLoan.objects.none()
        form = BookLoanForm(user=request.user)
        return render(request, 'library/BookLoan/view_loans.html', context={'loans': loans, 'form': form})

    query = request.GET.get('search', '')
    status_filters = request.GET.getlist('status')
    ordering = request.GET.get('ordering', '-loan_date') 

    loans = BookLoan.objects.filter(library=request.user.library)
    if query:
        loans = loans.filter(
            Q(books__title__icontains=query) | Q(books__author__icontains=query) |
            Q(person__name__icontains=query)
        )

    if status_filters and status_filters != ['']:
        loans = loans.filter(status__in=status_filters)
    else:
        status_filters = [status[0] for status in BookLoan._meta.get_field('status').choices]

    loans = loans.order_by(ordering)

    paginator = Paginator(loans, 30)
    page = request.GET.get('page')
    try:
        loan_paginated = paginator.page(page)
    except PageNotAnInteger:
        loan_paginated = paginator.page(1)
    except EmptyPage:
        loan_paginated = paginator.page(paginator.num_pages)

    loan_status_choices = BookLoan._meta.get_field('status').choices

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

    context = {
        'loans': loan_paginated,
        'query': query,
        'form': form,
        'selected_statuses': status_filters,
        'ordering': ordering,
        'loan_status_choices': loan_status_choices,
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