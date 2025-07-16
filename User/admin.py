from django.contrib import admin

from .models import CustomUser, Profile
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from library.models import Library

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'library')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'library')
    ordering = ('-date_joined',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['library'].queryset = Library.objects.all()
        return form