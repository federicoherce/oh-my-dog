from django.urls import path
from .views import solicitar_turno, turnos_cliente, turnos_veterinario, ver_turno, VerTurno

urlpatterns = [
    path('solicitar_turno', solicitar_turno, name='solicitar_turno'),
    path('turnos_cliente', turnos_cliente, name='turnos_cliente'),  # No me gusta el nombre, después lo discutimos
    path('turnos_veterinario', turnos_veterinario, name='turnos_veterinario'),
    path('ver_turno/<int:turno_id>', VerTurno.as_view(), name="ver_turno")
]