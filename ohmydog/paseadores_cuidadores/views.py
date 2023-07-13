# from django.views.generic import View
from .forms import CrearPaseadorCuidador, modificarPaseadorCuidador, crearValoracion
from .models import PaseadorCuidador, Valoracion
from .forms import CrearPaseadorCuidador, modificarPaseadorCuidador, ModificarPaseadorCuidadorSinTipo, ModificarValoracion
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


#def ha_realizado_valoracion(request, paseador_cuidador):
#    return Valoracion.objects.filter(paseador=paseador_cuidador, cliente= request.user).exists()

def listar_paseadores_cuidadores(request):
    paseadores_cuidadores = PaseadorCuidador.objects.all()

    if request.user.is_authenticated:
        valoraciones = Valoracion.objects.all()
    else:
        valoraciones = None
    if request.GET.get('tipo'):
        filtrado = request.GET['tipo']
        if filtrado != "":
            paseadores_cuidadores = PaseadorCuidador.objects.filter(tipo=filtrado)
    else:
        filtrado = ""
    for paseador_cuidador in paseadores_cuidadores:
        paseador_cuidador.promedio_valoraciones = paseador_cuidador.calcular_promedio_puntaje()
        if request.user.is_authenticated:
            paseador_cuidador.fue_valorado = paseador_cuidador.ha_realizado_valoracion(request)
    if request.method == "POST":
        pc_a_borrar = PaseadorCuidador.objects.get(email=request.POST['paseador_cuidador.email'], tipo=request.POST['paseador_cuidador.tipo'])
        pc_a_borrar.delete()
        return redirect("listar_paseadores_cuidadores")

    return render(request, "listar_paseadores_cuidadores.html", {
        'paseadores_cuidadores': paseadores_cuidadores,
        'filtrado': filtrado,
        #'ha_realizado_valoracion': ha_realizado_valoracion,
        'valoraciones': valoraciones,
    })

@user_passes_test(lambda u: u.is_superuser) 
def modificar_paseador_cuidador(request, email, tipo):
    paseador_cuidador = PaseadorCuidador.objects.get(email = email, tipo = tipo)
    paseadores = PaseadorCuidador.objects.filter(email=email)
    if request.method == "POST":
        form = modificarPaseadorCuidador(request.POST)
        if paseador_cuidador.tipo != request.POST.get('tipo') and (PaseadorCuidador.objects.filter(email=request.POST.get('email'), tipo=request.POST.get('tipo')).exists()):
            messages.error(request, "El email ya se encuentra registrado para este tipo")
            return render(request, "modificar_paseador_cuidador.html", {"form": form, "paseador_cuidador": paseador_cuidador})
        #return render(request, "modificar_paseador_cuidador.html", {"form": form, "paseador_cuidador": paseador_cuidador})
        if form.is_valid():
            paseador_cuidador.nomyap = request.POST.get('nomyap')
            paseador_cuidador.email = request.POST.get('email')
            paseador_cuidador.textolibre = request.POST.get('textolibre')
            paseador_cuidador.tipo = request.POST.get('tipo')
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
    pc = PaseadorCuidador.objects.get(id=pc_id)
    valoracion = Valoracion.objects.get(paseador=pc_id, cliente=request.user)

    if request.method == "POST":
        form = ModificarValoracion(request.POST, initial={'comentario': valoracion.comentario, 'puntaje': valoracion.puntaje})
        if form.is_valid():
            valoracion.comentario = form.cleaned_data['comentario']
            valoracion.puntaje = form.cleaned_data['puntaje']
            valoracion.save()
            messages.success(request, 'Valoracion modificada con exito')
            return redirect('listar_paseadores_cuidadores')
    else:
        form = ModificarValoracion(initial={'comentario': valoracion.comentario, 'puntaje': valoracion.puntaje})

    return render(request, "modificar_valoracion_paseador_cuidador.html", {"form": form, "paseador_cuidador": pc, "valoracion":valoracion})


@login_required
def eliminar_valoracion_paseador_cuidador(request, pc_id):
    valoracion = Valoracion.objects.get(paseador=pc_id, cliente=request.user)
    if request.method == 'POST':
            valoracion.delete()
    messages.success(request, 'Valoracion eliminada con exito')
    return redirect('listar_paseadores_cuidadores')


def perfil_paseador_cuidador(request, pc_id):
    paseador_cuidador = PaseadorCuidador.objects.get(id=pc_id)
    valoraciones = Valoracion.objects.filter(paseador=pc_id)
    paseador_cuidador.promedio_valoraciones = paseador_cuidador.calcular_promedio_puntaje()
    return render(request, "perfil_paseador_cuidador.html", {"paseador_cuidador":paseador_cuidador, "valoraciones":valoraciones})
