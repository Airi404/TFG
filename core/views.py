from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'core/home.html')

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loguea al usuario automáticamente
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})
