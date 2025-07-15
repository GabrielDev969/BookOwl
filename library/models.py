from django.db import models

class Book(models.Model):

    class StatusBook(models.TextChoices):
        AVAILABLE = 'available', 'Disponível'
        UNAVAILABLE = 'unavailable', 'Indisponível'
        CHECKED_OUT = 'checked_out', 'Emprestado'
        RESERVED = 'reserved', 'Reservado'

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=StatusBook.choices,
        default=StatusBook.AVAILABLE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.book.title} loaned to {self.person.name}"