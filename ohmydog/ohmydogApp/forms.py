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
    def __init__(self, *args, **kwargs):
        super(AgregarVeterinaria, self).__init__(*args, **kwargs)
        self.fields['calle'].initial = 'Calle '
    
    detalle = forms.CharField(
            required=False,
            label='Detalle (opcional)',
            widget=forms.Textarea(attrs={'placeholder': 'Piso, Departamento, Horario etc.'})
        )
    nro_calle = forms.CharField(label='Número')
    

    class Meta:
        model = Veterinaria
        exclude = ['longitud', 'latitud']

class EditarVeterinaria(forms.ModelForm):
     detalle = forms.CharField(required=False, label='Detalle (opcional)')
     nro_calle = forms.IntegerField(label='Número')

     class Meta:
         model = Veterinaria
         exclude = ['longitud', 'latitud']
    
     def __init__(self, *args, **kwargs):
         veterinaria = kwargs.pop('veterinaria')
         super(EditarVeterinaria, self).__init__(*args, **kwargs)
         self.fields['nombre'].initial = veterinaria.nombre
         self.fields['calle'].initial = veterinaria.calle
         self.fields['nro_calle'].initial = veterinaria.nro_calle
         self.fields['detalle'].initial = veterinaria.detalle
    