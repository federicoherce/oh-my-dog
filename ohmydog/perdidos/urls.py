from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_perros_perdidos, name="ver_perros_perdidos"),
    path('publicar_perro_perdido', views.publicar_perro_perdido, name='publicar_perro_perdido'),
    path('modificar_perro_perdido/<str:id>', views.modificar_perro_perdido, name='modificar_perro_perdido'),
    path('modificar_imagen/<str:id>', views.modificar_imagen, name='modificar_imagen'),
    path('marcar_perro_encontrado/<str:id>', views.marcar_perro_encontrado, name='marcar_perro_encontrado')
]