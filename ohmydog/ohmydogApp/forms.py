from django import forms
from perros.models import Vacuna

class tipoVacuna(forms.ModelForm):
    class Meta:
        model = Vacuna
        exclude = ['fecha', 'libreta_sanitaria']