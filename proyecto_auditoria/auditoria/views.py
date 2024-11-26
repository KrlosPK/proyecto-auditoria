from django.shortcuts import render, get_object_or_404
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


@login_required(login_url="auth/login_user/")
def diseño(request, codigo_control):
    control = get_object_or_404(Controles, codigo_control=codigo_control)
    return render(request, "diseño.html", {"control": control})
