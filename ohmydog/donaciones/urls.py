from django.urls import path
from .views import agregar_campana, ver_campana, eliminar_campana, realizar_donacion, ver_donaciones, donaciones_veterinaria, donaciones_campana

urlpatterns = [
    path('agregar_campana', agregar_campana, name='agregar_campana'),
    path('ver_campana', ver_campana, name='ver_campana'),
    path('eliminar_campana', eliminar_campana, name='eliminar_campana'),
    path('realizar_donacion/<str:tipo>', realizar_donacion, name='realizar_donacion'),
    path('ver_donaciones', ver_donaciones, name='ver_donaciones'),
    path('donaciones_veterinaria', donaciones_veterinaria, name='donaciones_veterinaria'),
    path('donaciones_campana', donaciones_campana, name='donaciones_campana')
]