from django.urls import path
from .views import ver_estadisticas, estadisticas_dinamicas

urlpatterns = [
    path('', ver_estadisticas, name='ver_estadisticas')
]