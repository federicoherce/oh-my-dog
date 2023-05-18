from typing import Any, Dict, Mapping, Optional, Type, Union
from django.db.models.query import QuerySet
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponse
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailAuthenticationForm, FiltrosDeListadoDeClientes, CambiarEmailForm, modificarDatosCliente
from django.contrib.auth.decorators import login_required, user_passes_test
from perros.models import Perro, LibretaSanitaria, Vacuna
from django.views.generic import ListView, DetailView
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail


# Create your views here.

@user_passes_test(lambda u: u.is_superuser) 
def registro(request):
    if (request.user.is_superuser == False):
        return redirect("home")
    
    password = CustomUser.objects.make_random_password(length=5, 
    allowed_chars='abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            msj = 'Gracias por registrarse en Oh My Dog, su contraseña es: ' + password
            send_mail('Registro Oh My Dog', msj, 'ohmydogg.vet@gmail.com', [email])
            return redirect('agregar_perro', form.cleaned_data['dni'])
        else:
            return render(request, "registro.html", {"form": form, "contra": password})
    else:
        form = CustomUserCreationForm()
        return render(request, 'registro.html', {"form": form, "contra": password}) 

    
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
            messages.error(request, "Email o contraseña invalidos")
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
            messages.success(request, 'Su contraseña se ha modificado con exito')
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
                messages.success(request, 'Su email se ha modificado con exito')
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
@user_passes_test(lambda u: u.is_superuser)
def lista_de_clientes(request):
    if (request.user.is_superuser == False):
        return redirect("home")
    queryset = CustomUser.objects.filter(is_superuser=False)
    nombre = request.GET.get('nombre')
    apellido = request.GET.get('apellido')
    dni = request.GET.get('dni')
    if nombre:
        queryset = queryset.filter(nombre__icontains=nombre) 
    if apellido:
        queryset = queryset.filter(apellido__icontains=apellido)
    if dni:
        queryset = queryset.filter(dni__icontains=dni)
    
    form = FiltrosDeListadoDeClientes()
    context = {
        'clientes' : queryset,
        'form' : form
    }
    return render(request, "listado_de_clientes.html", context)

# Del veterinario:
def ver_perfil_cliente(request, dni):
    if (request.user.is_superuser == False):
            return redirect("home")

    cliente = CustomUser.objects.get(dni=dni)
    return render(request, "perfil_cliente.html", {"cliente": cliente})

# Del veterinario:
def ver_perros_cliente(request, dni):
    if (request.user.is_superuser == False):
        return redirect("home")

    cliente = CustomUser.objects.get(dni=dni)
    perros = Perro.objects.filter(dueño=cliente)
    libretas_sanitaras = LibretaSanitaria.objects.filter(perro__in=perros)
    vacunas = Vacuna.objects.filter(libreta_sanitaria__in=libretas_sanitaras)

    if request.method == "POST":
        perro_id = request.POST.get('mascota_id')
        if perros.filter(id=perro_id).exists():
            perro_a_borrar = Perro.objects.get(id=perro_id)
            perro_a_borrar.delete()
            redirect("perros_cliente", dni=dni)

    return render(request, "perros_cliente.html", {
        "cliente": cliente,
        "mascotas": perros,
        "libretas_sanitarias": libretas_sanitaras,
        "vacunas": vacunas,
    })

@user_passes_test(lambda u: u.is_superuser) 
def modificar_datos_cliente(request, dni_url):
    if (request.user.is_superuser == False):
        return redirect("home")
    
    cliente = CustomUser.objects.get(dni = dni_url)
    if request.method == "POST":
        form = modificarDatosCliente(request.POST)
        if form.is_valid():
            nuevoNombre = request.POST.get('nombre')
            nuevoApellido = request.POST.get('apellido')
            nuevoDni = request.POST.get('dni')
            nuevoTelefono = request.POST.get('telefono')
            todosLosTfnos = CustomUser.objects.exclude(telefono=cliente.telefono).values_list('telefono', flat=True)
            todosLosDnis = CustomUser.objects.exclude(dni=cliente.dni).values_list('dni', flat=True)
            if nuevoDni in todosLosDnis:
                messages.error(request, "El dni ya se encuentra registrado")
                return render(request, "modificar_datos.html", {"form": form, "cliente": cliente})
            if nuevoTelefono in todosLosTfnos:
                messages.error(request, "El telefono ya se encuentra registrado")
                return render(request, "modificar_datos.html", {"form": form, "cliente": cliente})
            cliente.nombre = nuevoNombre
            cliente.apellido = nuevoApellido
            cliente.dni = nuevoDni
            cliente.telefono = nuevoTelefono
            cliente.save()
            messages.success(request, 'Datos modificados con exito')
            return redirect('perfil_cliente', cliente.dni)
    else:
        form = modificarDatosCliente()
    return render(request, "modificar_datos.html", {"form": form, "cliente": cliente})
