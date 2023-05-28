from django.urls import path
from .views import pagar_turno, pagar_con_tarjeta

app_name = 'pagos'

urlpatterns = [
    path('pagar_turno', pagar_turno, name='pagar_turno'),
    path('pagar_con_tarjeta', pagar_con_tarjeta, name='pagar_con_tarjeta')
]