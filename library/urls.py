from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('books/', views.view_books, name='view_books'),
    path('books/<int:book_id>/', views.details_book, name='details_book'),
]