from django import forms
from .models import Turno
from perros.models import Perro
from django.utils import timezone
from datetime import date

class SolicitarTurnoForm(forms.Form):
    MOTIVO_CHOICES = [
        ('vacuna', 'Vacuna'),
        ('vacuna_antirrabica', 'Vacuna antirrabica'),
        ('desparasitacion', 'Desparasitación'),
        ('castracion', 'Castración'),
        ('urgencia', 'Urgencia'),
        ('consulta', 'Consulta general')
    ]

    HORARIO_CHOICES = [
        ('tarde', 'Tarde'),
        ('mañana', 'Mañana')
    ]

    perro = forms.ModelChoiceField(queryset=None)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.now().strftime('%Y-%m-%d')}))
    hora = forms.ChoiceField(choices=HORARIO_CHOICES)
    motivo = forms.ChoiceField(choices=MOTIVO_CHOICES)

    def __init__(self, cliente, *args, **kwargs):
        super(SolicitarTurnoForm, self).__init__(*args, **kwargs)
        self.fields['perro'].queryset = Perro.objects.filter(dueño=cliente)
        self.fields['fecha'].widget.attrs['initial'] = timezone.now().date()

    def clean(self):
        cleaned_data = super().clean()
        perro = cleaned_data.get('perro')
        motivo = cleaned_data.get('motivo')

        if perro and (date.today() - perro.fecha_de_nacimiento).days <= 120 and motivo == 'vacuna_antirrabica':
            raise forms.ValidationError('No puede solicitar un turno de vacuna antirrábica para un perro menor a 4 meses.')
        return cleaned_data

class ModificarTurnoForm(forms.Form):
    horarios = [
        ('mañana', 'Mañana'),
        ('tarde', 'Tarde')
    ]

    hora = forms.ChoiceField(choices=horarios, label="Horario")
    motivo = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        turno_horario = kwargs.pop('turno_horario', None)
        super(ModificarTurnoForm, self).__init__(*args, **kwargs)
        self.fields['hora'].initial = turno_horario