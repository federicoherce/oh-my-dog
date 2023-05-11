from typing import Any, Dict, Mapping, Optional, Type, Union
from django.db.models.query import QuerySet
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailAuthenticationForm, FiltrosDeListadoDeClientes, CambiarEmailForm
from django.contrib.auth.decorators import login_required
from perros.models import Perro, LibretaSanitaria, Vacuna
from django.views.generic import ListView, DetailView
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail

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
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            msj = 'Gracias por registrarse en Oh My Dog, su contraseña es: ' + password
            send_mail('Registro Oh My Dog', msj, 'ohmydogg.vet@gmail.com', [email])
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
            user = CustomUser.objects.get(email = nombre_usuario)
            if usuario is not None:
                login(request, usuario)
                if user.get_activo():
                    return redirect('home')
                else:
                    return redirect('cambiarContra')
        else:
            messages.error(request, "información incorrecta")
    form=EmailAuthenticationForm()
    return render(request, "login.html", {"form": form}) 

@login_required      
def cambiarContra(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # no cierra sesion
            user = CustomUser.objects.get(email = request.user)
            user.activo = True
            user.save()
            return redirect("/")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "cambiarContra.html", {"form": form})

@login_required
def cambiarEmail(request):
    mensaje_error = ' '
    formulario = CambiarEmailForm()
    if request.method == 'POST':
        formulario = CambiarEmailForm(data=request.POST)
        if formulario.is_valid():
            nuevoEmail = request.POST.get('email')
            todosLosEmails = CustomUser.objects.values_list('email', flat=True)
            if nuevoEmail not in todosLosEmails:
                user = CustomUser.objects.get(email = request.user)
                user.email = nuevoEmail
                user.save()
                return redirect('/')
            else:
                messages.error(request, "Ese email ya se encuentra registrado")
    return render(request, 'cambiarEmail.html', {"form": formulario})


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

