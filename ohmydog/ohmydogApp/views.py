from django.shortcuts import render, HttpResponse, redirect
from turnos.models import Turno
from datetime import date 
from django.contrib import messages

def home(request):
    turnos = Turno.objects.filter(fecha=date.today(), estado="aceptado") 
    return render(request, "home.html", {"user": request.user, "turnos": turnos})



def confirmar_asistencia(request, turno_id, asistio):
    turno = Turno.objects.get(id=turno_id)
    if asistio == 'false':
        turno.cliente_asistio = False
        turno.save()
        messages.success(request, 'Se ha registrado la inasistencia del cliente')
        return redirect('home')
    else:
        turno.cliente_asistio = True
        turno.save() 
        messages.success(request, 'Se ha registrado la asistencia del cliente')
        return redirect('home')