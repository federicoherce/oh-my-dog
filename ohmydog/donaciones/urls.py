from django.urls import path
from .views import agregar_campaña

urlpatterns = [
    path('agregar_campaña', agregar_campaña, name='agregar_campaña')
]