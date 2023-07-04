"""ohmydog URL Configuration

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
from django.contrib import admin
from django.urls import path, include 
from ohmydogApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('confimar_asistencia/<int:turno_id>/<str:asistio>',
    views.confirmar_asistencia, name= "confirmar_asistencia"),
    path('actualizar_libreta/<int:turno_id>', views.actualizar_libreta, name="actualizar_libreta"),
    path('autenticacion/', include('autenticacion.urls')),
    path('perros/', include('perros.urls')),
    path('paseadores_cuidadores/', include('paseadores_cuidadores.urls')),
    path('adopcion/', include('adopcion.urls')),
    path('turnos/', include('turnos.urls')),
    path('pagos/', include('pagos.urls')),
    path('cruza/', include('cruza.urls')),
    path('donaciones/', include('donaciones.urls')),
    path('estadisticas/', include('estadisticas.urls')),
    path('perdidos/', include('perdidos.urls')),
    path('contactos/', views.ver_contactos, name="contactos"),
    path('contactos/editar/telefono', views.editar_telefono, name="contacto_editar_telefono"),
    path('contactos/editar/mail', views.editar_mail, name="contacto_editar_mail"),
    path('contactos/editar/<str:nombre_red_social>', views.editar_red_social, name="contacto_editar_red_social")
]



urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)