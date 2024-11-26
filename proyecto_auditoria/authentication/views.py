from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect


def redirect_if_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper


@redirect_if_authenticated
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        year = request.POST.get("year")
        period = request.POST.get("period")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session["año_control"] = year
            request.session["periodo_control"] = period

            auth_login(request, user)
            return redirect("home")
        else:
            messages.success(request, "Usuario o contraseña incorrectos")
            return redirect("login")
    else:
        current_year = datetime.now().year
        years = list(range(2022, current_year + 1))
        years.reverse()
        return render(request, "login.html", {"years": years})


def logout_user(request):
    auth_logout(request)
    messages.success(request, "Cierre de sesión exitoso")

    return redirect("login")
