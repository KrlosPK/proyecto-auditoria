from .models import (
    Controles,
    Diseño,
    Encabezado,
    Validaciones_Diseño,
    Validaciones_Diseño_Diseño,
)
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

    diseño = Diseño.objects.filter(control_id=control.id).first()

    validaciones_diseño = Validaciones_Diseño.objects.all()

    respuestas_validaciones = Validaciones_Diseño_Diseño.objects.filter(diseño=diseño)

    validaciones_con_respuestas = []
    for validacion in validaciones_diseño:
        respuesta = respuestas_validaciones.filter(
            validaciones_diseño=validacion
        ).first()
        validaciones_con_respuestas.append(
            {
                "validacion": validacion,
                "respuesta": respuesta,
            }
        )

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

            # Procesar validaciones y determinar la conclusión
            conclusion = "No Evaluado"  # Default
            for validacion in validaciones_diseño:
                respuesta_key = f"answer_{validacion.id}"
                explicacion_key = f"explanation_{validacion.id}"

                respuesta = request.POST.get(respuesta_key, "").strip()
                explicacion = request.POST.get(explicacion_key, "").strip()

                # Guardar o actualizar en la tabla pivote
                if respuesta or explicacion:
                    validacion_diseño_diseño, created = (
                        Validaciones_Diseño_Diseño.objects.get_or_create(
                            diseño=diseño,
                            validaciones_diseño=validacion,
                            defaults={
                                "respuesta_validacion": respuesta,
                                "explicacion_validacion": explicacion,
                            },
                        )
                    )
                    if not created:  # Actualizar si ya existe
                        validacion_diseño_diseño.respuesta_validacion = respuesta
                        validacion_diseño_diseño.explicacion_validacion = explicacion
                        validacion_diseño_diseño.save()

                # Determinar la conclusión
                if respuesta == "No":
                    conclusion = "Insatisfactorio"
                elif respuesta == "No aplica":
                    conclusion = "Insatisfactorio"
                elif conclusion != "Insatisfactorio" and respuesta == "Si":
                    conclusion = "Satisfactorio"

            diseño.conclusion_diseño = conclusion
            diseño.save()

            messages.success(request, "Diseño actualizado exitosamente.")
            return redirect("diseño", codigo_control=codigo_control)
        else:
            errores_formateados = "\n".join(errores.values())

            messages.error(request, errores_formateados)

    return render(
        request,
        "diseño.html",
        {
            "control": control,
            "diseño": diseño,
            "errores": errores,
            "validaciones_con_respuestas": validaciones_con_respuestas,
        },
    )


@login_required(login_url="auth/login_user/")
def encabezado(request, codigo_control):
    control = get_object_or_404(Controles, codigo_control=codigo_control)

    encabezado = Encabezado.objects.filter(control_id=control).first()

    errores = {}

    if request.method == "POST":
        fecha_elaboracion = request.POST.get("production_date", "")
        estado = request.POST.get("state", "")
        total_horas_invertidas = request.POST.get("total_hours_invested", "")
        recursos_consultados = request.POST.get("resources_consulted", "")

        if not fecha_elaboracion:
            errores["production_date"] = "El campo Fecha Elaboración es obligatorio."
        if not estado:
            errores["state"] = "El campo Estado es obligatorio."
        if not total_horas_invertidas:
            errores["total_hours_invested"] = (
                "El total de horas invertidas es obligatorio."
            )
        if total_horas_invertidas and total_horas_invertidas < "0":
            errores["total_hours_invested"] = (
                "El total de horas invertidas debe ser mayor o igual a 0."
            )
        if not recursos_consultados:
            errores["resources_consulted"] = (
                "Los recursos consultados son obligatorios."
            )
        else:
            try:
                fecha_elaboracion = datetime.strptime(
                    fecha_elaboracion, "%m/%d/%Y"
                ).strftime("%Y-%m-%d")
            except ValueError:
                errores["production_date"] = "El formato de la fecha es inválido."

        if not errores:
            if encabezado:
                encabezado.fecha_elaboracion = fecha_elaboracion
                encabezado.estado = estado
                encabezado.total_horas_invertidas = total_horas_invertidas
                encabezado.recursos_consultados = recursos_consultados

                messages.success(request, "Encabezado actualizado exitosamente.")

            else:
                encabezado = Encabezado(
                    control_id=control.id,
                    fecha_elaboracion=fecha_elaboracion,
                    estado=estado,
                    total_horas_invertidas=total_horas_invertidas,
                    recursos_consultados=recursos_consultados,
                )

                messages.success(request, "Encabezado creado exitosamente.")

            encabezado.save()

            return redirect("encabezado", codigo_control=codigo_control)
        else:
            errores_formateados = "\n".join(errores.values())

            messages.error(request, errores_formateados)

            return redirect("encabezado", codigo_control=codigo_control)

    return render(
        request,
        "encabezado.html",
        {"control": control, "encabezado": encabezado, "errores": errores},
    )
