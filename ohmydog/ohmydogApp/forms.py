from django import forms
from perros.models import Vacuna
from .models import Veterinaria

class tipoVacuna(forms.ModelForm):
    class Meta:
        model = Vacuna
        exclude = ['fecha', 'libreta_sanitaria']

class EditarTelefonoContacto(forms.Form):
    telefono = forms.CharField(label="Telefono", max_length=100)

    def __init__(self, *args, **kwargs):
        telefono_initial = kwargs.pop('telefono', '')
        super(EditarTelefonoContacto, self).__init__(*args, **kwargs)
        self.fields['telefono'].initial = telefono_initial

class EditarMailContacto(forms.Form):
    mail = forms.EmailField(label="Correo Electrónico", max_length=100)

    def __init__(self, *args, **kwargs):
        mail_initial = kwargs.pop('mail', '')
        super(EditarMailContacto, self).__init__(*args, **kwargs)
        self.fields['mail'].initial = mail_initial

class EditarRedSocial(forms.Form):
    enlace = forms.URLField(label='Enlace', max_length=200, widget=forms.URLInput(attrs={'class': 'form-control'}))

class AgregarVeterinaria(forms.ModelForm):
    detalle = forms.CharField(
            required=False,
            label='Detalle (*)',
            widget=forms.Textarea(attrs={'placeholder': 'Piso, Departamento, etc.'})
        )
    nro_calle = forms.IntegerField(label='Número')

    class Meta:
        model = Veterinaria
        exclude = ['longitud', 'latitud']
    