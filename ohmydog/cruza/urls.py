from django.urls import path
from .views import ver_perros_cruza

urlpatterns = [
    path('', ver_perros_cruza, name='ver_perros_cruza')
]