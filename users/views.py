from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.forms import CustomUserCreationForm

# Create your views here.
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