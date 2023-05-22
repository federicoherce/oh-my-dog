from django.urls import path
from .views import solicitar_turno, turnos_cliente

urlpatterns = [
    path('solicitar_turno', solicitar_turno, name='solicitar_turno'),
    path('turnos_cliente', turnos_cliente, name='turnos_cliente')  # No me gusta el nombre, después lo discutimos
]