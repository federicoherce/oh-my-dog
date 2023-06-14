from django.urls import path
from .views import agregar_campana, ver_campana, eliminar_campana, realizar_donacion

urlpatterns = [
    path('agregar_campana', agregar_campana, name='agregar_campana'),
    path('ver_campana', ver_campana, name='ver_campana'),
    path('eliminar_campana', eliminar_campana, name='eliminar_campana'),
    path('realizar_donacion/<str:tipo>', realizar_donacion, name='realizar_donacion')
]