from django.urls import path
from .views import agregar_perro

urlpatterns = [
    path('agregar_perro/<str:dni>/<str:password>', agregar_perro, name='agregar_perro')
]