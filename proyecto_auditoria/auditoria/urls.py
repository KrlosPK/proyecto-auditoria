from django.urls import path
from . import views

urlpatterns = [
    path("", views.controles, name="home"),
]
