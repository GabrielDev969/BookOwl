from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm

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
            user = form.save(commit=False)
            user.is_active = True            
            user.save()

            messages.success(request, "Account created.")
            return redirect('login')
    else:
        form = SignUpForm()
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

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'User/profile.html', context)