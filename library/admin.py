from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    search_fields = ('title', 'status')
    list_filter = ('created_at',)
    ordering = ('-created_at',)