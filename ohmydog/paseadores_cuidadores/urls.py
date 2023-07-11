from django.urls import path
from .views import agregar_paseador_cuidador, listar_paseadores_cuidadores, modificar_paseador_cuidador, valorar_paseador_cuidador, modificar_valoracion_paseador_cuidador, perfil_paseador_cuidador, eliminar_valoracion_paseador_cuidador

urlpatterns = [
    path('agregar_paseador_cuidador', agregar_paseador_cuidador, name='agregar_paseador_cuidador'),
    path('listar_paseadores_cuidadores', listar_paseadores_cuidadores, name='listar_paseadores_cuidadores'),
    path('modificar_paseador_cuidador/<str:email>/<str:tipo>', modificar_paseador_cuidador, name='modificar_paseador_cuidador'),
    path('valorar_paseador_cuidador/<int:pc_id>', valorar_paseador_cuidador, name='valorar_paseador_cuidador'),
    path('modificar_valoracion_paseador_cuidador/<int:pc_id>', modificar_valoracion_paseador_cuidador, name='modificar_valoracion_paseador_cuidador'),
    path('perfil_paseador_cuidador/<int:pc_id>', perfil_paseador_cuidador, name='perfil_paseador_cuidador'),
    path('eliminar_valoracion_paseador_cuidador/<int:pc_id>', eliminar_valoracion_paseador_cuidador, name='eliminar_valoracion_paseador_cuidador'),
]