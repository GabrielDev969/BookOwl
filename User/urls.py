from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('signup/', views.signup_close, name="signup"),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
]