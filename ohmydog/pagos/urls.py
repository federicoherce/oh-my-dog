from django.urls import path
from .views import pagar_turno, pagar_con_tarjeta, escanear_qr

app_name = 'pagos'

urlpatterns = [
    path('pagar_turno', pagar_turno, name='pagar_turno'),
    path('pagar_con_tarjeta/<int:monto>', pagar_con_tarjeta, name='pagar_con_tarjeta'),
    path('escanear_qr/<int:monto>', escanear_qr, name='escanear_qr')
]