from django import forms
from django.db import models 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):    
    class Meta:
        model = CustomUser
        fields = ('email', 'nombre', 'apellido', 'dni', 'telefono',)
        
        
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("email"),
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    
class CambiarEmailForm(forms.Form):
    email = forms.EmailField()
    


    