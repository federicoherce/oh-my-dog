from django.views.generic import View
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Campaña, Donacion
from .forms import CrearCampaña, CrearDonacion
from django.db.models import Sum

# Create your views here.
def agregar_campana(request):
    if request.method == "POST":
        form = CrearCampaña(request.POST)
        if form.is_valid():
            Campaña.objects.create(nombre=request.POST['nombre'], 
                                 monto_objetivo=request.POST['monto_objetivo'],
                                 descripcion=request.POST['descripcion'])
            return redirect('home')
    else:
        form = CrearCampaña()
    return render(request, 'agregar_campana.html', {
        'form': form
    })


def ver_campana(request):
    campana = Campaña.objects.first()

    return render(request, 'ver_campana.html', 
            {'campana': campana}
        )

def eliminar_campana(request):
    campana = Campaña.objects.first()

    if request.method == 'POST':
        campana.delete()
        donaciones_campaña = Donacion.objects.filter(tipo='Campaña')
        donaciones_campaña.delete()
    
    return redirect('home')

def realizar_donacion(request, tipo):
    if request.method == "POST":
        monto = request.POST.get('monto')
        nombre = request.POST.get('nombre')
        if nombre == '':
            nombre = 'Zz'
        form = CrearDonacion(request.POST)
        if form.is_valid():
            return redirect('pagos:pagar_donacion', monto=monto, nombre=nombre, tipo=tipo)
    else:
        form = CrearDonacion()
    return render(request, 'realizar_donacion.html', {
        'form': form
    })
    
def ver_donaciones(request):
    return render(request, "ver_donaciones.html")

def donaciones_veterinaria(request):
    donaciones_vet = Donacion.objects.filter(tipo='Veterinaria')
    total_monto = Donacion.objects.aggregate(total=Sum('monto'))['total']
    return render(request, 'donaciones_veterinaria.html', {
                "donaciones": donaciones_vet,
                "total_monto": total_monto})
    
def donaciones_campana(request):
    return render(request, 'donaciones_campana.html')