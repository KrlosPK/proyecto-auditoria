from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_controles, name="home"),
    path("diseño/<str:codigo_control>", views.diseño, name="diseño"),
    path("encabezado/<str:codigo_control>", views.encabezado, name="encabezado"),
]
