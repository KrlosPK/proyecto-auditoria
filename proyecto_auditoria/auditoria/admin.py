from django.contrib import admin

from .models import (
    Controles,
    Diseño,
    Validaciones_Diseño,
    Validaciones_Diseño_Diseño,
    Auditores,
    Encabezado,
)

admin.site.register(Controles)
admin.site.register(Diseño)
admin.site.register(Validaciones_Diseño)
admin.site.register(Validaciones_Diseño_Diseño)
admin.site.register(Auditores)
admin.site.register(Encabezado)
