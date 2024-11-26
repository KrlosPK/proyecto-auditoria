from django.db import models
from django.contrib.auth.models import User


class Auditores(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    correo = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=20)
    cargo = models.CharField(max_length=150)
    area = models.CharField(max_length=150)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuarios")

    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre


class Controles(models.Model):
    nombre_control = models.CharField(max_length=150)
    codigo_control = models.CharField(max_length=20)
    estado_control = models.CharField(max_length=20)
    conclusion_control = models.TextField()
    descripcion_control = models.TextField()
    frecuencia_control = models.CharField(max_length=20)
    clasificacion_control = models.CharField(max_length=20)
    tipologia_control = models.CharField(max_length=20)
    descripcion_riesgo = models.TextField()
    preventivo_detectivo = models.CharField(max_length=20)
    objetivo_control = models.TextField()

    auditor = models.ForeignKey(Auditores, on_delete=models.CASCADE)

    año_control = models.IntegerField()
    periodo_control = models.IntegerField()

    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre_control


class Validaciones_Diseño(models.Model):
    pregunta_validacion = models.CharField(max_length=150)
    respuesta_validacion = models.CharField(max_length=10, blank=True)
    explicacion_validacion = models.TextField()

    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.pregunta_validacion


class Diseño(models.Model):
    responsable_diseño = models.CharField(max_length=150)
    comentarios_diseño = models.TextField()

    control = models.OneToOneField(
        Controles, on_delete=models.CASCADE, related_name="diseño"
    )

    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.responsable_diseño


class Validaciones_Diseño_Diseño(models.Model):
    validaciones_diseño = models.ForeignKey(
        Validaciones_Diseño, on_delete=models.CASCADE
    )
    diseño = models.ForeignKey(Diseño, on_delete=models.CASCADE)

    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.validaciones_diseño


class Encabezado(models.Model):
    estado = models.CharField(max_length=30)
    total_horas_invertidas = models.IntegerField()
    recursos_consultados = models.TextField()

    control = models.OneToOneField(
        Controles, on_delete=models.CASCADE, related_name="encabezado"
    )

    fecha_elaboracion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.estado
