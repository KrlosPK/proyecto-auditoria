from .models import Controles, Diseño
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


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

    errores = {}

    if request.method == "POST":
        responsable_diseño = request.POST.get("design_responsible", "")
        comentarios_diseño = request.POST.get("design_commments", "")
        fecha_ejecucion_prueba = request.POST.get("test_execution_date", "")

        if not responsable_diseño:
            errores["design_responsible"] = (
                "El campo Responsable de Diseño es obligatorio."
            )
        if not comentarios_diseño:
            errores["design_commments"] = "El campo Comentarios es obligatorio."
        if not fecha_ejecucion_prueba:
            errores["test_execution_date"] = (
                "La Fecha de Ejecución de la Prueba es obligatoria."
            )
        else:
            try:
                fecha_ejecucion_prueba = datetime.strptime(
                    fecha_ejecucion_prueba, "%m/%d/%Y"
                ).strftime("%Y-%m-%d")
            except ValueError:
                errores["test_execution_date"] = "El formato de la fecha es inválido."

        if not errores:
            if diseño:
                diseño.responsable_diseño = responsable_diseño
                diseño.comentarios_diseño = comentarios_diseño
                diseño.fecha_ejecucion_prueba = fecha_ejecucion_prueba

                messages.success(request, "Diseño actualizado exitosamente.")

            else:
                diseño = Diseño(
                    control_id=control.id,
                    responsable_diseño=responsable_diseño,
                    comentarios_diseño=comentarios_diseño,
                    fecha_ejecucion_prueba=fecha_ejecucion_prueba,
                )

                messages.success(request, "Diseño creado exitosamente.")
            diseño.save()
            return redirect("diseño", codigo_control=codigo_control)
        else:
            errores_formateados = "\n".join(errores.values())

            messages.error(request, errores_formateados)

            return redirect("diseño", codigo_control=codigo_control)

    return render(
        request,
        "diseño.html",
        {"control": control, "diseño": diseño, "errores": errores},
    )
