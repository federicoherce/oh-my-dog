from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import PerroCruza
from autenticacion.models import CustomUser
from perros.models import Perro
from django.contrib import messages
from .forms import PublicarPerroCruzaForm
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from ohmydog.decorators import veterinario_restringido


def ver_perros_cruza(request):
    perros_cruza = PerroCruza.objects.all()
    return render(request, 'index_cruza.html', 
            {'perros_cruza': perros_cruza}
        )

@veterinario_restringido
def publicar_perro(request):
    if request.method == "POST":
        form = PublicarPerroCruzaForm(request.POST, request.user)
        cliente = request.user  
        perro_id = request.POST.get('perro')
        perro = Perro.objects.get(id=perro_id)
        if perro.sexo != 'macho':
            return redirect('seleccionar_fecha_celo', perro)
        perro_cruza = PerroCruza.objects.create(dueño=cliente, perro=perro)
        perro_cruza.save()
        messages.success(request, 'Perro publicado con exito')
        return redirect('ver_perros_cruza')
    else:
        perros = Perro.objects.filter(dueño=request.user).exclude(id__in=PerroCruza.objects.values('perro_id'))
        form = PublicarPerroCruzaForm()
        return render(request, 'publicar_perro_cruza.html', {"perros": perros, "form": form})


@veterinario_restringido
def enviar_solicitud_cruce(request, perro, autor, sexo, id):
    if request.method == "POST":
        perro_id = request.POST.get('perro')
        perro_select = Perro.objects.get(id=perro_id)
        sexo_perro = perro_select.sexo
        if sexo_perro != sexo:
            publicado_por = CustomUser.objects.get(id=autor)
            interesado = request.user.email
            asunto_interesado = "Solicitud enviada"
            msj_interesado = "Su solicitud de cruce fue enviada con exito, espere a que el dueño se ponga en contacto con usted"
            send_mail(asunto_interesado, msj_interesado, 'ohmydogg.vet@gmail.com', [interesado])
            
            asunto_autor = "Han solicitado un cruce con tu perro/a"
            msj_autor = interesado + " ha solicitado realizar una cruza con " + perro + ". Comuníquese con el para concretar el cruce"
            send_mail(asunto_autor, msj_autor, "ohmydogg.vet@gmail.com", [publicado_por.email])
            messages.success(request, 'Su solicitud fue enviada con exito')
            return redirect('ver_perros_cruza')
        else:
            messages.error(request, "Los perros tienen el mismo sexo, selecciona otro de tus perros.")
    perros_cliente = PerroCruza.objects.filter(dueño=request.user)
    return render(request, "enviar_solicitud_cruce.html",{
        "perros": perros_cliente,
        "nombre": perro, 
        "autor": autor,
        "sexo": sexo,
        "perro_id": id})


@veterinario_restringido
def enviar_solicitud_recomendada(request, perro, autor):
    perro_cliente = Perro.objects.get(id=perro)
    publicado_por = CustomUser.objects.get(id=autor)
    interesado = request.user.email
    asunto_interesado = "Solicitud enviada"
    msj_interesado = "Su solicitud de cruce fue enviada con exito, espere a que el dueño se ponga en contacto con usted"
    send_mail(asunto_interesado, msj_interesado, 'ohmydogg.vet@gmail.com', [interesado])
    asunto_autor = "Han solicitado un cruce con tu perro/a"
    msj_autor = interesado + " ha solicitado realizar una cruza con " + perro_cliente.nombre + ". Comuníquese con el para concretar el cruce"
    send_mail(asunto_autor, msj_autor, "ohmydogg.vet@gmail.com", [publicado_por.email])
    messages.success(request, 'Su solicitud fue enviada con exito')
    return redirect('ver_perros_cruza')


@veterinario_restringido
def recomendar_perro(request):
    if request.method == "POST":
        perro_selected = PerroCruza.objects.get(perro=request.POST.get('perro'))
        perro_recommended = get_recomendacion(perro_selected)
        if perro_recommended == None:
            messages.error(request, "Lo sentimos, no encontramos una buena recomendación para que cruces a tu perro en este momento.")
        else:
            messages.success(request, "Hemos encontrado una recomendacion adecuada para tu perro")
            return redirect('ver_perro', perro_recommended.id, perro_selected.id)
    perros_cliente = PerroCruza.objects.filter(dueño=request.user)
    return render(request, "recomendar_perro.html", {
        "perros": perros_cliente
    })


def get_recomendacion(perro_selected):

    perros_compatibles = PerroCruza.objects.filter(
        perro__raza=perro_selected.perro.raza,
        perro__sexo="hembra" if perro_selected.perro.sexo == "macho" else "macho",
    )

    return perros_compatibles.first()


def ver_perro(request, perro, perro_cliente):
    recomendado = False
    if perro_cliente != "-1":
        recomendado = True
    perro_cruza = PerroCruza.objects.get(id=perro)
    perros_cliente = PerroCruza.objects.filter(dueño=request.user)
    return render(request, "ver_perro.html", 
                  {"perro": perro_cruza, 
                   "recomendado": recomendado,
                   "perros_cliente": perros_cliente})


def seleccionar_fecha_celo(request, perro):
    if request.method == 'POST':
        form = PublicarPerroCruzaForm(request.POST, request.user)
        if form.is_valid():
            fecha_celo = request.POST.get('celo')
            cliente = request.user
            perroAC = Perro.objects.get(nombre=perro)
            perro_cruza = PerroCruza.objects.create(dueño=cliente, perro=perroAC, fecha_de_celo=fecha_celo)
            perro_cruza.save()
            messages.success(request, 'Perro publicado con exito')
            return redirect('ver_perros_cruza')
    else:
        form = PublicarPerroCruzaForm()
    return render(request, 'seleccionar_fecha_celo.html', {'form':form, 'perro':perro})
