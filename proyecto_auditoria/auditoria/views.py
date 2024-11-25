from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required(login_url="auth/login_user/")

# Create your views here.
def controles(request):
    return render(request, "controles.html", {})
