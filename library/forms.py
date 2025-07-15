from django import forms
from .models import Book, Person, BookLoan
from django.db import models

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

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

class BookLoanForm(forms.ModelForm):
    status_loan = forms.ChoiceField(
        choices=[
            ('checked_out', 'Checked Out'),
            ('reserved', 'Reservado'),
        ],
        label='Status do Empréstimo',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = BookLoan
        fields = ['book', 'person', 'return_date']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'person': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(status='available')
        if self.instance and self.instance.pk and self.instance.book:
            self.fields['book'].queryset = Book.objects.filter(
                models.Q(status='avaliable') | models.Q(pk=self.instance.book.pk)
            )

    def save(self, commit=True):
        loan = super().save(commit=False)
        if self.cleaned_data['return_date']:
            loan.book.status = 'available'
        else:
            loan.book.status = self.cleaned_data['status_loan']
        loan.book.save()
        if commit:
            loan.save()
        return loan