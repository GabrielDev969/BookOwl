from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser, Profile
from library.models import Library

class SignUpCloseForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True, help_text='Por favor, forneça um e-mail válido.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Digite seu primeiro nome.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Digite seu sobrenome.')
    library_name = forms.CharField(max_length=100, required=True, help_text='Digite o nome da biblioteca.')

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


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True, help_text='Por favor, forneça um e-mail válido.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Digite seu primeiro nome.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Digite seu sobrenome.')
    library_name = forms.CharField(max_length=100, required=True, help_text='Digite o nome da biblioteca.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name','library_name', 'password1', 'password2')

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

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Senha Antiga",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha atual'}),
    )

    new_password1 = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua nova senha'}),
    )

    new_password2 = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua nova senha'}),
    )

    class Meta:
        fields=['old_password', 'new_password1', 'new_password2']

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'autofocus': True})

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('A senha antiga está incorreta.')
        return old_password