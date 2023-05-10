from django.shortcuts import render, redirect
# from django.views.generic import View
from .forms import CrearPerro
from .models import Perro, LibretaSanitaria
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def agregar_perro(request):
    if request.method == "POST":
        form = CrearPerro(request.POST)
        if form.is_valid():
            p = Perro.objects.create(nombre=request.POST['nombre'], 
                                 raza=request.POST['raza'],
                                 color=request.POST['color'],
                                 fecha_de_nacimiento=request.POST['fecha_de_nacimiento'],
                                 dueño=request.user)
            LibretaSanitaria.objects.create(perro=p)
            return redirect('home')    # Debería redirigirlo al perfil del usuario
    else:
        form = CrearPerro()
    return render(request, 'agregar_perro.html', {
        'form': form
    })