from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback')
]
