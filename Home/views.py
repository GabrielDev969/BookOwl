from django.shortcuts import render

def home(request):
    """
    Render the home page.
    """
    return render(request, 'Home/home.html')

def about(request):
    """
    Render the about page.
    """
    return render(request, 'Home/about.html')