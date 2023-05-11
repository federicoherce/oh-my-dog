"""proyectoWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from .views import registro, cerrar_sesion, loguear, cambiarContra, cambiarEmail, mi_perfil, mis_mascotas, ListaDeClientes, ver_perfil_cliente, ver_perros_cliente
from autenticacion import views
from .views import registro, cerrar_sesion, loguear, mi_perfil, mis_mascotas


urlpatterns = [
    path('', registro.as_view(), name='registro'),
    path('cerrar_sesion', cerrar_sesion, name='cerrar_sesion'),
    path('login', loguear , name='login'),
    path('cambiarContra', cambiarContra, name ='cambiarContra'),
    path('cambiarEmail', cambiarEmail, name ='cambiarEmail'),
    path('mi_perfil', mi_perfil, name='mi_perfil'),
    path('mi_perfil/mis_mascotas', mis_mascotas, name='mis_mascotas'),
    path('listado_de_clientes', ListaDeClientes.as_view(), name='listado_de_clientes'),
    path('perfil/<str:dni>', ver_perfil_cliente, name='perfil_cliente'),
    path('perfil/<str:dni>/perros', ver_perros_cliente, name="perros_cliente"),
]
