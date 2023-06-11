from django.urls import path
from .views import ver_perros_cruza, publicar_perro, enviar_solicitud_cruce

urlpatterns = [
    path('', ver_perros_cruza, name='ver_perros_cruza'),
    path('publicar_perro_cruza', publicar_perro, name='publicar_perro_cruza'),
    path('enviar_solicitud_cruce/<str:perro>/<str:autor>/<str:sexo>',
    enviar_solicitud_cruce, name='enviar_solicitud_cruce')
]