from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import EmailAuthenticationForm
from django.contrib.auth.decorators import login_required
from perros.models import Perro, LibretaSanitaria, Vacuna

# Create your views here.


class registro(View):
    
    def get(self, request):
        form = CustomUserCreationForm()
        
        return render(request, 'registro.html', {"form": form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('agregar_perro')
        else:
            return render(request, "registro.html", {"form": form})
    
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def loguear(request):
        if request.method=="POST":
            form = EmailAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                nombre_usuario=form.cleaned_data.get("username")
                contra=form.cleaned_data.get("password")
                usuario=authenticate(username=nombre_usuario, password=contra)
                if usuario is not None:
                    login(request, usuario)
                    return redirect('home')
                else:
                    messages.error(request, "usuario no válido")
            else:
                messages.error(request, "información incorrecta")
        form=EmailAuthenticationForm()
        return render(request, "login.html", {"form": form}) 

@login_required
def mi_perfil(request):
    usuario = request.user
    return render(request, "mi_perfil.html", {
        'usuario': usuario
    })

@login_required
def mis_mascotas(request):
    mascotas = Perro.objects.filter(dueño=request.user)
    libretas_sanitarias = LibretaSanitaria.objects.filter(perro__in=mascotas)
    vacunas = Vacuna.objects.filter(libreta_sanitaria__in=libretas_sanitarias)
    return render(request, "mis_mascotas.html", {
        'mascotas': mascotas,
        'libretas_sanitarias': libretas_sanitarias,
        'vacunas': vacunas
    })
