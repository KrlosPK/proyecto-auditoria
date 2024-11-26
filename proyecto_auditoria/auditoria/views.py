from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Controles, Diseño


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

    diseño = Diseño.objects.filter(control_id=control).first()

    if request.method == "POST":
        responsable_diseño = request.POST.get("design_responsible", "")
        comentarios_diseño = request.POST.get("design_commments", "")
        fecha_ejecucion_prueba = request.POST.get("test_execution_date", "")

        if diseño:
            diseño.responsable_diseño = responsable_diseño
            diseño.comentarios_diseño = comentarios_diseño
            diseño.fecha_ejecucion_prueba = fecha_ejecucion_prueba
        else:
            diseño = Diseño(
                control_id=control,
                responsable_diseño=responsable_diseño,
                comentarios_diseño=comentarios_diseño,
                fecha_ejecucion_prueba=fecha_ejecucion_prueba,
            )

        diseño.save()
        return redirect("diseño", codigo_control=codigo_control)

    return render(request, "diseño.html", {"control": control, "diseño": diseño})
