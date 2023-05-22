from django.urls import path
from .views import publicar, listar_perros_adopcion, marcar_Adoptado, eliminar_perro_en_adopcion, enviar_solicitud_adopcion

urlpatterns = [
    path('perros_en_adopcion', listar_perros_adopcion, name="perros_en_adopcion"),
    path('publicar/', publicar, name='publicar_perro'),
    path('cliente/<int:perro_id>/marcar_Adoptado/', marcar_Adoptado, name='marcar_Adoptado'),
    path('cliente/<int:perro_id>/eliminar/', eliminar_perro_en_adopcion, name='eliminar_perro_en_adopcion'),
    path('enviar_solicitud/<int:autor>/<int:interesado>/<str:perro>/',
    enviar_solicitud_adopcion, name="enviar_solicitud_adopcion"),
]