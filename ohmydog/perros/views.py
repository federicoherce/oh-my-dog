from django.shortcuts import render, redirect
# from django.views.generic import View
from .forms import CrearPerro
from .models import Perro, LibretaSanitaria
from django.contrib.auth.decorators import login_required, user_passes_test
from autenticacion.models import CustomUser
from django.core.mail import send_mail


# Create your views here.
def is_superuser(user):
    return user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='home')
def agregar_perro(request, dni, password):
    usuario = CustomUser.objects.get(dni=dni)
    if request.method == "POST":
        form = CrearPerro(request.POST)
        if form.is_valid():
            un_perro = Perro.objects.create(nombre=request.POST['nombre'], 
                                 raza=request.POST['raza'],
                                 color=request.POST['color'],
                                 fecha_de_nacimiento=request.POST['fecha_de_nacimiento'],
                                 sexo=request.POST['sexo'],
                                 dueño=usuario)
            LibretaSanitaria.objects.create(perro=un_perro)
            if usuario.get_usuario_nuevo():
                msj = 'Gracias por registrarse en Oh My Dog, su contraseña es: ' + password
                send_mail('Registro Oh My Dog', msj, 'ohmydogg.vet@gmail.com', [usuario.email])
                usuario.usuario_nuevo = False
                usuario.save()
            return redirect("perros_cliente", usuario.dni)
    else:
        form = CrearPerro()
    return render(request, 'agregar_perro.html', {
        'form': form
    })