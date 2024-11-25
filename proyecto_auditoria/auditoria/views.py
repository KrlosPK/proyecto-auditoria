from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Controles


@login_required(login_url="auth/login_user/")
def all_controles(request):
    controles_list = Controles.objects.all()

    return render(request, "controles.html", {"controles": controles_list})
