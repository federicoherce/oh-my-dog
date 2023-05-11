from typing import Any, Dict, Mapping, Optional, Type, Union
from django.db.models.query import QuerySet
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailAuthenticationForm, FiltrosDeListadoDeClientes
from django.contrib.auth.decorators import login_required
from perros.models import Perro, LibretaSanitaria, Vacuna
from django.views.generic import ListView, DetailView
from .models import CustomUser

# Create your views here.

# Del veterinario:
class registro(View):
    
    def get(self, request):
        form = CustomUserCreationForm()
        
        return render(request, 'registro.html', {"form": form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('agregar_perro', usuario)
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

# Del cliente:
@login_required
def mi_perfil(request):
    usuario = request.user
    return render(request, "mi_perfil.html", {
        'usuario': usuario
    })

# Del cliente:
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

# Del veterinario:
class ListaDeClientes(ListView):
    model = CustomUser
    template_name = "listado_de_clientes.html"
    context_object_name = "clientes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FiltrosDeListadoDeClientes()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.GET.get('nombre')
        apellido = self.request.GET.get('apellido')
        dni = self.request.GET.get('dni')

        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if apellido:
            queryset = queryset.filter(apellido__icontains=apellido)
        if dni:
            queryset = queryset.filter(dni__icontains=dni)
        return queryset

# Del veterinario:
def ver_perfil_cliente(request, dni):
    cliente = CustomUser.objects.get(dni=dni)
    return render(request, "perfil_cliente.html", {"cliente": cliente})

# Del veterinario:
def ver_perros_cliente(request, dni):
    cliente = CustomUser.objects.get(dni=dni)
    perros = Perro.objects.filter(dueño=cliente)
    libretas_sanitaras = LibretaSanitaria.objects.filter(perro__in=perros)
    vacunas = Vacuna.objects.filter(libreta_sanitaria__in=libretas_sanitaras)

    if request.method == "POST":
        perro_a_borrar = get_object_or_404(Perro, id=request.POST['mascota_id'])
        perro_a_borrar.delete()
        redirect("perros_cliente", cliente)

    return render(request, "perros_cliente.html", {
        "cliente": cliente,
        "mascotas": perros,
        "libretas_sanitarias": libretas_sanitaras,
        "vacunas": vacunas,
    })

