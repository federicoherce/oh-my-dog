from django.urls import path
from .views import agregar_paseador_cuidador, listar_paseadores_cuidadores

urlpatterns = [
    path('agregar_paseador_cuidador', agregar_paseador_cuidador, name='agregar_paseador_cuidador'),
    path('listar_paseadores_cuidadores', listar_paseadores_cuidadores, name='listar_paseadores_cuidadores')
]