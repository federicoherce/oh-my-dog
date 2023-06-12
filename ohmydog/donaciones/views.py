from django.views.generic import View
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Campaña
from .forms import CrearCampaña

# Create your views here.
def agregar_campaña(request):
    if request.method == "POST":
        form = CrearCampaña(request.POST)
        if form.is_valid():
            Campaña.objects.create(nombre=request.POST['nombre'], 
                                 monto_objetivo=request.POST['monto_objetivo'],
                                 descripcion=request.POST['descripcion'])
            return redirect('home')
    else:
        form = CrearCampaña()
    return render(request, 'agregar_campaña.html', {
        'form': form
    })