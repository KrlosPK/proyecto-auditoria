from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Controles


@login_required(login_url="auth/login_user/")
def all_controles(request):
    anio_control_session = request.session.get("año_control", None)
    periodo_control_session = request.session.get("periodo_control", None)

    controles_list = Controles.objects.filter(
        año_control=anio_control_session, periodo_control=periodo_control_session
    ).order_by("id")

    return render(request, "controles.html", {"controles": controles_list})
