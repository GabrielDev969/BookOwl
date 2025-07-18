from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('books/', views.view_books, name='view_books'),
    path('books/<int:book_id>/', views.details_book, name='details_book'),
    path('people/', views.view_peoples, name='view_peoples'),
    path('people/<int:person_id>/', views.details_people, name='details_people'),
    path('loans/', views.view_loans, name='view_loans'),
    path('loans/<int:loan_id>/', views.details_loan, name='details_loan'),
    path('loans/cancel/<int:loan_id>/', views.cancel_loan, name='cancel_loan'),
    path('loans/return/<int:loan_id>/', views.returned_loan, name='returned_loan'),
    path('loans/pickup/<int:loan_id>/', views.pickup_loan, name='pickup_loan'),
]