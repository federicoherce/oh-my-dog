from django.urls import path
from .views import solicitar_turno, turnos_cliente, turnos_veterinario, VerTurnoVeterinario, ver_turno_cliente

urlpatterns = [
    path('solicitar_turno', solicitar_turno, name='solicitar_turno'),
    path('turnos_cliente', turnos_cliente, name='turnos_cliente'),  # No me gusta el nombre, después lo discutimos
    path('turnos_veterinario', turnos_veterinario, name='turnos_veterinario'),
    path('ver_turno_veterinario/<int:turno_id>', VerTurnoVeterinario.as_view(), name="ver_turno_veterinario"),
    path('ver_turno_cliente/<int:turno_id>', ver_turno_cliente, name='ver_turno_cliente')
]