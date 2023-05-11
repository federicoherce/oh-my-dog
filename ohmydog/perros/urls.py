from django.urls import path
from .views import agregar_perro

urlpatterns = [
    path('agregar_perro/<str:dni>', agregar_perro, name='agregar_perro')
]