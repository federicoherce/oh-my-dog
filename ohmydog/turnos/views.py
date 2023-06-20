from typing import Any
from django import http
from django.shortcuts import render, redirect
from .models import Turno
from .forms import SolicitarTurnoForm, ModificarTurnoForm
from perros.models import Perro
from autenticacion.models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views import View
from django.core.mail import send_mail
from datetime import date
from django.utils import timezone
from django.utils.decorators import method_decorator
from ohmydog.decorators import veterinario_required



# Create your views here.
def is_superuser(user):
    return user.is_superuser

@login_required(login_url='login')
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
            turno.cliente_asistio = None
            turno.save()
            messages.success(request, "El turno fue solicitado con éxito. Un veterinario lo revisará pronto.")
            return redirect("solicitar_turno")
        else:
            messages.error(request, 'No se puede solicitar un turno de vacuna antirrábica para un perro menor de 4 meses.')
            return redirect("solicitar_turno")
    else:
        form = SolicitarTurnoForm(request.user)

    return render(request, 'solicitar_turno.html', {'form': form})

@login_required(login_url='login')
def turnos_cliente(request):
    cliente_actual = request.user.id
    turnos = Turno.objects.filter(cliente=cliente_actual).order_by('fecha')
    filtrado = ""
    if request.GET.get('fecha'):
        filtrado = request.GET['fecha']
        if filtrado == 'pasado':
            turnos = turnos.filter(fecha__lt=date.today())
        elif filtrado == 'futuro':
            turnos = turnos.filter(fecha__gte=date.today())
    return render(request, "turnos_cliente.html", {
        'turnos': turnos,
        'filtrado': filtrado
    })

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='home')
def turnos_veterinario(request):
    turnos = Turno.objects.all().order_by('fecha')
    if request.GET.get('estado'):
        filtrado = request.GET['estado']
        if filtrado != "":
            turnos = turnos.filter(estado=filtrado)
        return render(request, 'turnos_veterinario.html', {"turnos": turnos, "filtrado": filtrado})
    fecha_actual = timezone.now().date()
    turnos = Turno.objects.filter(fecha__gte=fecha_actual).order_by('fecha')
    turnos_pasados = Turno.objects.filter(fecha__lt=fecha_actual).order_by('fecha')
    turnos = list(turnos) + list(turnos_pasados)
    filtrado = ""
    return render(request, 'turnos_veterinario.html', {"turnos": turnos, "filtrado": filtrado})


@method_decorator(veterinario_required, name='dispatch')
class VerTurnoVeterinario(View):
    template = "ver_turno.html"

    #@method_decorator(user_passes_test(lambda u: u.is_superuser))
    #def dispatch(self, request, *args, **kwargs):
    #    return super().dispatch(request, *args, **kwargs)

    def get(self, request, turno_id):
        turno = Turno.objects.get(id=turno_id)
        form = ModificarTurnoForm(turno_horario=turno.hora)
        context = {
            'turno': turno,
            'form': form
        }
        return render(request, self.template, context)

    def post(self, request, turno_id):
        turno = Turno.objects.get(id=turno_id)
        form = ModificarTurnoForm(request.POST or None, turno_horario=turno.hora)

        accion = request.POST.get('accion')
        if accion == 'Aceptar':
            turno.estado = 'aceptado'
            turno.save()
            msj = f"""
                Su turno para el día {turno.fecha} en el horario {turno.hora} cuyo motivo es {turno.motivo} ha sido aceptado.
            """
            cliente = CustomUser.objects.get(email=turno.cliente)
            send_mail('Turno aceptado', msj, 'ohmydogg.vet@gmail.com', [cliente.email])
            messages.success(request, "Turno aceptado. Se le envío un mail al cliente sobre el estado del turno")
            return redirect('turnos_veterinario')
        elif accion == 'Rechazar':
            turno.estado = 'rechazado'
            turno.cliente_asistio = False
            turno.save()
            msj = f"""
                Su turno para el día {turno.fecha} en el horario {turno.hora} cuyo motivo es {turno.motivo} ha sido rechazado.
            """
            cliente = CustomUser.objects.get(email=turno.cliente)
        ## turno.delete()
            send_mail('Turno rechazado', msj, 'ohmydogg.vet@gmail.com', [cliente.email])
            messages.success(request, "Turno rechazado con éxito. Se le envío un mail al cliente sobre el estado del turno")
            return redirect('turnos_veterinario')
        elif accion == 'Guardar cambios' and form.is_valid():
                msj = f"""
                    Su turno para el día {turno.fecha} en el horario {turno.hora} cuyo motivo es {turno.motivo} ha sido modificado para el horario {form.cleaned_data['hora']}.
                    Motivo de la modificación del turno: {form.cleaned_data['motivo']}
                    Puede aceptar o rechazar la modificación del turno a través del sitio web.
                """
                turno.hora = form.cleaned_data['hora']
                turno.estado = 'modificado'
                turno.save()
                cliente = CustomUser.objects.get(email=turno.cliente)
                send_mail('Turno modificado', msj, 'ohmydogg.vet@gmail.com', [cliente.email])
                messages.success(request, 'Turno modificado con éxito. Se le envío un mail al cliente sobre el estado del turno.')
                return redirect('turnos_veterinario')
        context = {
            'turno': turno,
            'form': form,
        }
        return render(request, self.template, context)

@login_required(login_url='login') 
def ver_turno_cliente(request, turno_id):
    turno = Turno.objects.get(id=turno_id)
    if request.method == 'POST':
        accion = request.POST.get('action')
        if accion == "Aceptar":
            turno.estado = "aceptado"
            msj_feedback = "Modificación de turno aceptada. Ya puede acudir al turno."
        elif accion == "Rechazar":
            print('rechazo')
            msj_feedback = "Modificación de turno rechazada. Deberá solicitar un nuevo turno."
            turno.estado = "rechazado"
        else:
            msj_feedback = "No se realizaron cambios en el estado del turno"
        turno.save()
        messages.success(request, msj_feedback)
        return redirect('turnos_cliente')
    return render(request, "ver_turno_cliente.html", {'turno': turno})