from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):

    class StatusBook(models.TextChoices):
        AVAILABLE = 'available', 'Disponível'
        UNAVAILABLE = 'unavailable', 'Indisponível'
        CHECKED_OUT = 'checked_out', 'Emprestado'
        RESERVED = 'reserved', 'Reservado'

    library = models.ForeignKey(Library, on_delete=models.CASCADE)
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
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class BookLoan(models.Model):

    class StatusLoan(models.TextChoices):
        ACTIVE = 'active', 'Ativo'
        OVERDUE = 'overdue', 'Atrasado'
        RETURNED = 'returned', 'Devolvido'
        RESERVED = 'reserved', 'Reservado'
        CANCELLED = 'cancelled', 'Cancelado'

    cd_bookloan = models.PositiveIntegerField(
        editable=False,
        verbose_name='N° do Empréstimo',
    )

    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name='loans')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)
    date_previous_return = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=StatusLoan.choices,
        default=StatusLoan.ACTIVE,
    )

    class Meta:
        unique_together = ('library', 'cd_bookloan')
        ordering = ['-cd_bookloan']

    def __str__(self):
        book_title = ", ".join(book.title for book in self.book.all())
        return f"{book_title} loaned to {self.person.name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            last_loan = BookLoan.objects.filter(library=self.library).order_by('-cd_bookloan').first()

            if last_loan:
                self.cd_bookloan = last_loan.cd_bookloan + 1
            else:
                self.cd_bookloan = 1
        super().save(*args, **kwargs)