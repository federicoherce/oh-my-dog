from django.urls import path
from .views import ver_perros_cruza, publicar_perro, enviar_solicitud_cruce, recomendar_perro, ver_perro, enviar_solicitud_recomendada, seleccionar_fecha_celo

urlpatterns = [
    path('', ver_perros_cruza, name='ver_perros_cruza'),
    path('publicar_perro_cruza', publicar_perro, name='publicar_perro_cruza'),
    path('enviar_solicitud_cruce/<str:perro>/<str:autor>/<str:sexo>/<str:id>',
    enviar_solicitud_cruce, name='enviar_solicitud_cruce'),
    path('enviar_solicitud_recomendada/<str:perro>/<str:autor>/',
    enviar_solicitud_recomendada, name='enviar_solicitud_recomendada'),
    path('recomendacion', recomendar_perro, name='recomendar_perro'),
    path('ver_perro/<str:perro>/<str:perro_cliente>', ver_perro, name='ver_perro'),
    path('seleccionar_fecha_celo/<str:perro>', seleccionar_fecha_celo, name='seleccionar_fecha_celo')
]