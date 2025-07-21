from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, SignUpCloseForm, CustomPasswordChangeForm

class CustomLoginView(LoginView):
    template_name = 'User/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

@transaction.atomic
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True            
            user.save()

            messages.success(request, "Account created.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'User/signup.html', {'form': form})

def signup_close(request):
    messages.info(request, 'Não estamos recebendo cadastros no momentos.')
    if request.method == 'POST':
        return redirect('login')
    else:
        form = SignUpCloseForm()
    return render(request, 'User/signup.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Instancia os dois formulários com os dados enviados (request.POST) e arquivos (request.FILES)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        # Valida ambos os formulários
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('profile') # Redireciona para a mesma página de perfil

    else:
        # Se for um GET, apenas instancia os formulários com os dados atuais do usuário
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        form = CustomPasswordChangeForm(user=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': form
    }

    return render(request, 'User/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('profile')
        else:
            messages.error(request, 'Erro ao alterar a senha. Verifique os dados e tente novamente.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'password_form': form,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'User/profile.html', context)