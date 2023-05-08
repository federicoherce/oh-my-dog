from django.urls import path
from .views import agregar_perro

urlpatterns = [
    path('agregar_perro', agregar_perro, name='agregar_perro')
]