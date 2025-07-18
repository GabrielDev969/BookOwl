from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')), 
    path('auth/', include('User.urls')),
    path('library/', include('library.urls')),
]
