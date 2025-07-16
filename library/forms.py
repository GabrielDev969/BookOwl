from django import forms
from .models import Book, Person, BookLoan
from django.db import models

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
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
    status_loan = forms.ChoiceField(
        choices=[
            ('checked_out', 'Emprestado'),
            ('reserved', 'Reservado'),
        ],
        label='Status do Empréstimo',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = BookLoan
        fields = ['books', 'person', 'return_date']
        widgets = {
            'books': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'person': forms.Select(attrs={'class': 'form-control'}),
            'return_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
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

    def clean(self):
        cleaned_data = super().clean()
        books = cleaned_data.get('books')
        person = cleaned_data.get('person')
        return_date = cleaned_data.get('return_date')

        if self.user and hasattr(self.user, 'library') and self.user.library:
            if books:
                for book in books:
                    if book.library != self.user.library:
                        raise forms.ValidationError(f"O livro '{book.title}' não pertence à sua biblioteca.")
                    if not return_date and BookLoan.objects.filter(
                        books=book, return_date__isnull=True
                    ).exclude(pk=self.instance.pk).exists():
                        raise forms.ValidationError(f"O livro '{book.title}' já está emprestado ou reservado e não foi devolvido.")
            if person and person.library != self.user.library:
                raise forms.ValidationError("A pessoa selecionada não pertence à sua biblioteca.")
        
        if self.instance and self.instance.pk and self.instance.return_date:
            raise forms.ValidationError("Este empréstimo não pode ser editado porque a data de devolução já foi definida.")
        
        return cleaned_data

    def save(self, commit=True):
        loan = super().save(commit=False)
        if self.user and hasattr(self.user, 'library') and self.user.library:
            loan.library = self.user.library
        loan.status_loan = self.cleaned_data['status_loan'] if not self.cleaned_data['return_date'] else 'available'
        if commit:
            loan.save()
            if self.cleaned_data['books']:
                loan.books.set(self.cleaned_data['books'])
                for book in self.cleaned_data['books']:
                    book.status = loan.status_loan
                    book.save()
        return loan