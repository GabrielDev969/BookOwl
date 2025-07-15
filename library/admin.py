from django.contrib import admin
from .models import Book, Person, BookLoan
from .forms import BookLoanForm

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    search_fields = ('title', 'status')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    form = BookLoanForm
    list_display = ('book', 'person', 'loan_date', 'return_date')
    search_fields = ('book__title', 'person__name')
    list_filter = ('loan_date', 'return_date')
    ordering = ('-loan_date',)