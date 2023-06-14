from django.urls import path
from .views import pagar_turno, pagar_con_tarjeta, escanear_qr, pagar_donacion

app_name = 'pagos'

urlpatterns = [
    path('pagar_turno/<int:dni>', pagar_turno, name='pagar_turno'),
    path('pagar_con_tarjeta/<str:monto>/<int:dni>', pagar_con_tarjeta, name='pagar_con_tarjeta'),
    path('pagar_donacion/<str:monto>/<str:nombre>/<str:tipo>', pagar_donacion, name='pagar_donacion'),
    path('escanear_qr/<str:monto>/<int:dni>', escanear_qr, name='escanear_qr')
]