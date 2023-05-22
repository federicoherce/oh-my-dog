from django.shortcuts import render, redirect
from .models import Turno
from .forms import SolicitarTurnoForm
from perros.models import Perro
from autenticacion.models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Create your views here.
@login_required
def solicitar_turno(request):
    if request.method == 'POST':
        form = SolicitarTurnoForm(request.user, request.POST)
        
        if form.is_valid():
            turno = Turno(
                cliente=request.user, 
                fecha=form.cleaned_data['fecha'],
                hora=form.cleaned_data['hora'],
                perro=form.cleaned_data['perro'],
                motivo=form.cleaned_data['motivo']
            )
            turno.save()
            messages.success(request, "El turno fue solicitado con éxito. Un veterinario lo revisará pronto.")
            return redirect("solicitar_turno")
        else:
            messages.error(request, 'No se puede solicitar un turno de vacuna antirrábica para un perro menor de 4 meses.')
            return redirect("solicitar_turno")
    else:
        form = SolicitarTurnoForm(request.user)

    return render(request, 'solicitar_turno.html', {'form': form})

@login_required
def turnos_cliente(request):
    return render(request, 'turnos_cliente.html')