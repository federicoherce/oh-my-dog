from django.urls import path
from .views import publicar, listado

urlpatterns = [
    path('', listado, name="perros_en_adopcion"),
    path('publicar/', publicar, name='publicar_perro'),
]