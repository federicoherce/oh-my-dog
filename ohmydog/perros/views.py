from django.shortcuts import render, redirect
# from django.views.generic import View
from .forms import CrearPerro
from .models import Perro, LibretaSanitaria
from django.contrib.auth.decorators import login_required
from autenticacion.models import CustomUser

# Create your views here.
@login_required
def agregar_perro(request, dni):
    usuario = CustomUser.objects.get(dni=dni)
    if request.method == "POST":
        form = CrearPerro(request.POST)
        if form.is_valid():
            p = Perro.objects.create(nombre=request.POST['nombre'], 
                                 raza=request.POST['raza'],
                                 color=request.POST['color'],
                                 fecha_de_nacimiento=request.POST['fecha_de_nacimiento'],
                                 dueño=usuario)
            LibretaSanitaria.objects.create(perro=p)
            return redirect("perros_cliente", usuario.dni)
    else:
        form = CrearPerro()
    return render(request, 'agregar_perro.html', {
        'form': form
    })