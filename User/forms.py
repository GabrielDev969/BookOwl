from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile
from library.models import Library

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True, help_text='Please provide a valid email.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Enter your last name.')
    library_name = forms.CharField(max_length=100, required=True, help_text='Enter the name of the library.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name','library_name', 'password1', 'password2')

    def __init__(self ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['disabled'] = True
        self.fields['first_name'].widget.attrs['disabled'] = True
        self.fields['last_name'].widget.attrs['disabled'] = True
        self.fields['library_name'].widget.attrs['disabled'] = True
        self.fields['username'].widget.attrs['disabled'] = True
        self.fields['password1'].widget.attrs['disabled'] = True
        self.fields['password2'].widget.attrs['disabled'] = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            library_name = self.cleaned_data.get('library_name')
            library = Library.objects.create(name=library_name)
            user.library = library
            user.save()
            user.profile.first_name = self.cleaned_data['first_name']
            user.profile.last_name = self.cleaned_data['last_name']
            user.profile.save()
        return user
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']