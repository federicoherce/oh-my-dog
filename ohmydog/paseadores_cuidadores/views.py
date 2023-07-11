# from django.views.generic import View
from .forms import CrearPaseadorCuidador, modificarPaseadorCuidador, crearValoracion
from .models import PaseadorCuidador, Valoracion
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
    paseadores_cuidadores = PaseadorCuidador.objects.all()
    if request.user.is_authenticated:
        def ha_realizado_valoracion(paseador):
            return Valoracion.objects.filter(paseador=paseador, cliente=request.user).exists()
        paseadores_con_valoracion = [(paseador, ha_realizado_valoracion(paseador)) for paseador in paseadores_cuidadores]
        valoraciones = Valoracion.objects.all()
    else:
        paseadores_con_valoracion = paseadores_cuidadores
    if request.GET.get('tipo'):
        filtrado = request.GET['tipo']
        if filtrado != "":
            paseadores_con_valoracion = PaseadorCuidador.objects.filter(tipo=filtrado)
    else:
        filtrado = ""
    if request.method == "POST":
        pc_a_borrar = PaseadorCuidador.objects.get(email=request.POST['paseador_cuidador.email'])
        pc_a_borrar.delete()
        redirect("listar_paseadores_cuidadores")

    return render(request, "listar_paseadores_cuidadores.html", {
        'paseadores_cuidadores': paseadores_con_valoracion,
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

@login_required
def valorar_paseador_cuidador(request, pc_id):
    pc = PaseadorCuidador.objects.get(id = pc_id)
    if request.method == "POST":
        form = crearValoracion(request.POST)
        if form.is_valid():
            puntajeJS = request.POST['puntaje']
            Valoracion.objects.create(comentario = request.POST['comentario'], cliente = request.user, paseador = pc, puntaje = puntajeJS)
            messages.success(request, 'Valoracion agregada con exito')
            return redirect('listar_paseadores_cuidadores')
    else:
        form = crearValoracion()
    return render(request, "valorar_paseador_cuidador.html", {"form": form, "paseador_cuidador": pc})

@login_required
def modificar_valoracion_paseador_cuidador(request, pc_id):

    return render(request, "modificar_valoracion_paseador_cuidador.html")


@login_required
def eliminar_valoracion_paseador_cuidador(request, pc_id):
    if request.method == "POST":
        d
    return render(request, "listar_paseadores_cuidadores.html")


def perfil_paseador_cuidador(request, pc_id):

    return render(request, "perfil_paseador_cuidador.html")
