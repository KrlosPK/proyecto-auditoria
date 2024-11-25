from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from datetime import datetime


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.success(request, "Usuario o contraseña incorrectos")
            # I don't want to redirect to the home page, I want to stay in the login page
            return redirect("login")
    else:
        current_year = datetime.now().year
        years = list(range(2022, current_year + 1))
        years.reverse()
        return render(request, "login.html", {"years": years})
