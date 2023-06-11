from django import forms
from datetime import date
from django.utils import timezone

class PublicarPerroCruzaForm(forms.Form):
    celo = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.now().strftime('%Y-%m-%d')}))