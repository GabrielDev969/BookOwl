from django import forms
from .models import Book, Person, BookLoan
from django.db import models
from django.utils import timezone

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        book = super().save(commit=False)
        if self.user and self.user.library:
            book.library = self.user.library
        if commit:
            book.save()
        return book

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        person = super().save(commit=False)
        if self.user and self.user.library:
            person.library = self.user.library
        if commit:
            person.save()
        return person

class BookLoanForm(forms.ModelForm):
    status_book = forms.ChoiceField(
        choices=[
            ('checked_out', 'Emprestado'),
            ('reserved', 'Reservado'),
        ],
        label='Status do Empréstimo',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = BookLoan
        fields = ['books', 'person', 'date_previous_return']
        widgets = {
            'books': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'person': forms.Select(attrs={'class': 'form-select'}),
            'date_previous_return': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if self.user and hasattr(self.user, 'library') and self.user.library:
            self.fields['books'].queryset = Book.objects.filter(library=self.user.library, status='available')
            self.fields['person'].queryset = Person.objects.filter(library=self.user.library)
        else:
            self.fields['books'].queryset = Book.objects.none()
            self.fields['person'].queryset = Person.objects.none()
        if self.instance and self.instance.pk and self.user and hasattr(self.user, 'library') and self.user.library:
            self.fields['books'].queryset = Book.objects.filter(
                models.Q(library=self.user.library, status='available') | models.Q(id__in=self.instance.books.all())
            )
            self.fields['person'].widget.attrs['disabled'] = True
            self.fields['books'].widget.attrs['disabled'] = True
            # Tornar books e person opcionais na edição
            self.fields['books'].required = False
            self.fields['person'].required = False
            # Garantir que status_book reflita o status do primeiro livro
            if self.instance.books.exists():
                first_book = self.instance.books.first()
                self.fields['status_book'].initial = first_book.status

    def clean(self):
        cleaned_data = super().clean()
        books = cleaned_data.get('books')
        person = cleaned_data.get('person')
        date_previous_return = cleaned_data.get('date_previous_return')

        if self.user and hasattr(self.user, 'library') and self.user.library:
            # Na edição, usar os livros existentes se books não for fornecido
            if self.instance and self.instance.pk and not books:
                books = self.instance.books.all()
            if books:
                for book in books:
                    if book.library != self.user.library:
                        raise forms.ValidationError(f"O livro '{book.title}' não pertence à sua biblioteca.")
                    if BookLoan.objects.filter(
                        books=book, return_date__isnull=True
                    ).exclude(pk=self.instance.pk).exists():
                        raise forms.ValidationError(f"O livro '{book.title}' já está emprestado ou reservado e não foi devolvido.")
            # Na edição, usar a pessoa existente se person não for fornecido
            if self.instance and self.instance.pk and not person:
                person = self.instance.person
            if person and person.library != self.user.library:
                raise forms.ValidationError("A pessoa selecionada não pertence à sua biblioteca.")
        
        if self.instance and self.instance.pk and self.instance.return_date:
            raise forms.ValidationError("Este empréstimo não pode ser editado porque a data de devolução já foi definida.")
        
        if date_previous_return and date_previous_return < timezone.now():
            raise forms.ValidationError("A data prevista de devolução deve ser no futuro.")

        # Atualizar cleaned_data com os valores existentes, se necessário
        cleaned_data['books'] = books
        cleaned_data['person'] = person
        return cleaned_data

    def save(self, commit=True):
        loan = super().save(commit=False)
        if self.user and hasattr(self.user, 'library') and self.user.library:
            loan.library = self.user.library
        loan.status_book = self.cleaned_data['status_book']
        if commit:
            loan.save()
            # Na criação, definir os livros; na edição, manter os existentes
            if self.cleaned_data['books']:
                loan.books.set(self.cleaned_data['books'])
            # Atualizar o status de todos os livros associados
            for book in loan.books.all():
                book.status = loan.status_book
                book.save()
        return loan