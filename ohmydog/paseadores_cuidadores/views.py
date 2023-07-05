# from django.views.generic import View
from .forms import CrearPaseadorCuidador, modificarPaseadorCuidador
from .models import PaseadorCuidador
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

# Create your views here.
@login_required
def agregar_paseador_cuidador(request):
    if request.method == "POST":
        form = CrearPaseadorCuidador(request.POST)
        if (PaseadorCuidador.objects.filter(email=request.POST.get('email'), tipo=request.POST.get('tipo')).exists()):
            messages.error(request, "El email ya se encuentra registrado para este tipo")
            return render(request, "agregar_paseador_cuidador.html", {"form": form})
        if form.is_valid():
            PaseadorCuidador.objects.create(nomyap=request.POST['nomyap'], 
                                 email=request.POST['email'],
                                 textolibre=request.POST['textolibre'],
                                 tipo=request.POST['tipo'])
            return redirect('listar_paseadores_cuidadores')
    else:
        form = CrearPaseadorCuidador()
    return render(request, 'agregar_paseador_cuidador.html', {
        'form': form
    })



def listar_paseadores_cuidadores(request):
    paseadores_cuidadores = PaseadorCuidador.objects.all

    if request.GET.get('tipo'):
        filtrado = request.GET['tipo']
        if filtrado != "":
            paseadores_cuidadores = PaseadorCuidador.objects.filter(tipo=filtrado)
    else:
        filtrado = ""
    if request.method == "POST":
        pc_a_borrar = PaseadorCuidador.objects.get(email=request.POST['paseador_cuidador.email'])
        pc_a_borrar.delete()
        redirect("listar_paseadores_cuidadores")

    return render(request, "listar_paseadores_cuidadores.html", {
        'paseadores_cuidadores': paseadores_cuidadores,
        'filtrado': filtrado
    })

@user_passes_test(lambda u: u.is_superuser) 
def modificar_paseador_cuidador(request, email, tipo):
    paseador_cuidador = PaseadorCuidador.objects.get(email = email, tipo = tipo)
    if request.method == "POST":
        form = modificarPaseadorCuidador(request.POST)
        if (PaseadorCuidador.objects.filter(email=request.POST.get('email'), tipo=request.POST.get('tipo')).exists()):
            messages.error(request, "El email ya se encuentra registrado para este tipo")
            return render(request, "modificar_paseador_cuidador.html", {"form": form, "paseador_cuidador": paseador_cuidador})
        if form.is_valid():
            nuevoNomyap = request.POST.get('nomyap')
            nuevoEmail = request.POST.get('email')
            nuevoTextoLibre = request.POST.get('textolibre')
            nuevoTipo = request.POST.get('tipo')
            paseador_cuidador.nomyap = nuevoNomyap
            paseador_cuidador.email = nuevoEmail
            paseador_cuidador.textolibre = nuevoTextoLibre
            paseador_cuidador.tipo = nuevoTipo
            paseador_cuidador.save()
            messages.success(request, 'Datos modificados con exito')
            return redirect('listar_paseadores_cuidadores')
    else:
        form = modificarPaseadorCuidador()
    return render(request, "modificar_paseador_cuidador.html", {"form": form, "paseador_cuidador": paseador_cuidador})
