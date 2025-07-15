from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True, help_text='Please provide a valid email.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']