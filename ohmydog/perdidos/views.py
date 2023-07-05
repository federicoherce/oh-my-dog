from django.shortcuts import render, redirect
from .forms import PublicarPerroPerdido, ModificarPerroPerdido, ModificarImagen
from django.contrib import messages
from .models import Perdidos
from autenticacion.models import CustomUser


def ver_perros_perdidos(request):
    perros = Perdidos.objects.all()
    if request.GET.get('estado'):
        filtrado = request.GET['estado']
        if filtrado != "":
            perros = Perdidos.objects.filter(estado=filtrado)
    else:
        filtrado = ""
    return render(request, "ver_perros_perdidos.html", {
        "perros": perros,
        "filtrado": filtrado})

def publicar_perro_perdido(request):
    if request.method == 'POST':
        form = PublicarPerroPerdido(data=request.POST, files=request.FILES)
        if form.is_valid():
            perro = form.save(commit=False)
            perro.telefono = request.user.telefono
            form.save()
            messages.success(request, 'Perro publicado con éxito')
            return redirect('ver_perros_perdidos')
    else:
        form = PublicarPerroPerdido()
    return render(request, "publicar_perro_perdido.html", {"form": form})

def modificar_perro_perdido(request, id):
    perro = Perdidos.objects.get(id = id)
    if request.method == "POST":
        form = ModificarPerroPerdido(request.POST)
        if form.is_valid():
            nuevoNombre = request.POST.get('nombre')
            nuevaRaza= request.POST.get('raza')
            nuevoColor = request.POST.get('color')
            nuevoTamaño = request.POST.get('tamaño')
            nuevoSexo = request.POST.get('sexo')
            nuevoOrigen = request.POST.get('origen')
            nuevaObservacion = request.POST.get('observacion')
            nuevoEstado = request.POST.get('estado')
            perro.nombre = nuevoNombre
            perro.raza = nuevaRaza
            perro.color = nuevoColor
            perro.tamaño = nuevoTamaño
            perro.sexo = nuevoSexo
            perro.origen = nuevoOrigen
            perro.observacion = nuevaObservacion
            perro.estado = nuevoEstado
            perro.save()
            messages.success(request, 'Datos modificados con exito')
            return redirect('ver_perros_perdidos')
    else:
        form = ModificarPerroPerdido()
    return render(request, "modificar_perro_perdido.html", {"form": form, "perro": perro})


def modificar_imagen(request, id):
    if request.method == 'POST':
        form = ModificarImagen(request.POST, request.FILES)
        if form.is_valid():
            perro = Perdidos.objects.get(id = id)
            perro.imagen = form.cleaned_data['imagen']
            perro.save()
            messages.success(request, 'Imagen modificada con exito')
            return redirect('ver_perros_perdidos')
    else:
        form = ModificarImagen()
    return render(request, 'modificar_imagen.html', {'form': form})
