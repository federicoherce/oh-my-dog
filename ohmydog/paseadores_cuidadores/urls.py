from django.urls import path
from .views import agregar_paseador_cuidador

urlpatterns = [
    path('agregar_paseador_cuidador', agregar_paseador_cuidador, name='agregar_paseador_cuidador')
]