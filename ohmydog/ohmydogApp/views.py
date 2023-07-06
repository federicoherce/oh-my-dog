from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseNotFound, JsonResponse
from turnos.models import Turno
from perros.models import Perro, Vacuna, LibretaSanitaria
from donaciones.models import Campaña
from .forms import tipoVacuna, EditarTelefonoContacto, EditarMailContacto, EditarRedSocial, AgregarVeterinaria
from autenticacion.models import CustomUser
from datetime import date, timedelta
from django.contrib import messages
from .models import Veterinaria
import json
import requests
from django.core import serializers

def home(request):
    turnos = Turno.objects.filter(fecha=date.today(), estado__in=["aceptado"], cliente_asistio=None)
    turnosPendientes = Turno.objects.filter(estado="pendiente")
    
    latitud = 40.7128
    longitud = -74.0060
    latitud_pin1 = 40.712
    longitud_pin1 = -74.005
    latitud_pin2 = 40.713
    longitud_pin2 = -74.007
    
    return render(request, "home.html", {
        "user": request.user,
        "turnos": turnos,
        "pendientes": turnosPendientes,
        'latitud': latitud,
        'longitud': longitud,
        'latitud_pin1': latitud_pin1,
        'longitud_pin1': longitud_pin1,
        'latitud_pin2': latitud_pin2,
        'longitud_pin2': longitud_pin2
    })

#campana = Campaña.objects.first()
# "campana": campana}


def confirmar_asistencia(request, turno_id, asistio):
    turno = Turno.objects.get(id=turno_id)
    if asistio == 'false':
        turno.cliente_asistio = False
        turno.save()
        messages.success(request, 'Se ha registrado la inasistencia del cliente')
    else:
        turno.cliente_asistio = True
        turno.save() 
        messages.success(request, 'Se ha registrado la asistencia del cliente')
        if turno.motivo == 'vacuna':
            generarTurno(turno)
            return redirect('actualizar_libreta', turno_id)
        elif turno.motivo == 'vacuna_antirrabica':
            return redirect('actualizar_libreta', turno_id)
        else:
            return redirect('pagos:pagar_turno', turno.cliente.dni)
    return redirect('home')


def actualizar_libreta(request, turno_id):
    if request.method == "GET":
        form = tipoVacuna()
    else:
        form = tipoVacuna(request.POST)
        if form.is_valid():
            turno = Turno.objects.get(id=turno_id)
            vacuna = Vacuna(tipo=request.POST['tipo'])
            perro = Perro.objects.get(id=turno.perro_id)
            libreta = LibretaSanitaria.objects.get(perro_id=perro.id)
            vacuna.libreta_sanitaria = libreta
            vacuna.save()
            messages.success(request, 'Libreta actualizada')
            return redirect('pagos:pagar_turno', turno.cliente.dni)
    return render(request, "actualizar_libreta.html", {"form": form})

def generarTurno(turno):
    perro = Perro.objects.get(id=turno.perro_id)
    fecha_limite = date.today() - timedelta(days=4*30)
    if perro.fecha_de_nacimiento > fecha_limite: #el perro tiene menos de 4 meses de edad 
        nuevoTurno = Turno(
            cliente= CustomUser.objects.get(id=turno.cliente_id),
            fecha= date.today() + timedelta(days=21),
            hora=turno.hora,
            perro=perro,
            motivo=turno.motivo,
            estado = 'aceptado'
        )
        nuevoTurno.cliente_asistio = None
        nuevoTurno.save()
    else:   #el perro tiene 4 meses o mas 
        nuevoTurno = Turno(
            cliente= CustomUser.objects.get(id=turno.cliente_id),
            fecha= date.today() + timedelta(days=365),
            hora=turno.hora,
            perro=perro,
            motivo=turno.motivo,
            estado = 'aceptado'
        )
        nuevoTurno.cliente_asistio = None
        nuevoTurno.save()

def ver_contactos(request):
    return render(request, "ver_contactos.html")

def editar_mail(request):
    #with open("ohmydog/ohmydogApp/redes.json") as redes:
    with open("ohmydogApp/redes.json", "r") as redes:
        datos_redes = json.load(redes)
    mail = datos_redes['formas_contacto'][0]['dato']

    if request.method == "POST":
        form = EditarMailContacto(request.POST, mail)

        if form.is_valid():
            nuevo_mail = request.POST.get('mail')
            #with open("ohmydog/ohmydogApp/redes.json") as redes:
            with open("ohmydogApp/redes.json", "w") as redes:
                datos_redes['formas_contacto'][0]['dato'] = nuevo_mail
                json.dump(datos_redes, redes, indent=4)
            return redirect('contactos')
    
    form = EditarMailContacto(mail=mail)
    return render(request, 'editar_mail.html', {'form': form})
    
def editar_telefono(request):
    #with open("ohmydog/ohmydogApp/redes.json") as redes:
    with open("ohmydogApp/redes.json", "r") as redes:
        datos_redes = json.load(redes)
    telefono = datos_redes['formas_contacto'][1]['dato']

    if request.method == "POST":
        form = EditarTelefonoContacto(request.POST, telefono)

        if form.is_valid():
            nuevo_telefono = request.POST.get('telefono')
            #with open("ohmydog/ohmydogApp/redes.json") as redes:
            with open("ohmydogApp/redes.json", "w") as redes:
                datos_redes['formas_contacto'][1]['dato'] = nuevo_telefono
                json.dump(datos_redes, redes, indent=4)
            return redirect('contactos')
    
    form = EditarTelefonoContacto(telefono=telefono)
    return render(request, 'editar_mail.html', {'form': form})

def editar_red_social(request, nombre_red_social):
    #with open("ohmydog/ohmydogApp/redes.json") as redes:
    with open("ohmydogApp/redes.json", "r") as redes:
        datos_redes = json.load(redes)
    redes_sociales = datos_redes['redes_sociales']
    #red_seleccionada = redes_sociales[nombre_red_social]

    red_seleccionada = None
    for red_social in redes_sociales:
        if red_social['nombre'] == nombre_red_social:
            red_seleccionada = red_social
            break

    if red_seleccionada == None:
        return HttpResponseNotFound('Red social no encontrada')

    if request.method == "POST":
        form = EditarRedSocial(request.POST)

        if form.is_valid():
            nueva_url = form.cleaned_data['enlace']
            red_seleccionada['enlace'] = nueva_url

            #with open("ohmydog/ohmydogApp/redes.json") as redes:
            with open("ohmydogApp/redes.json", "w") as redes:
                json.dump(datos_redes, redes, indent=4)

            return redirect('contactos')
    
    form = EditarRedSocial(initial={'enlace': red_seleccionada['enlace']})
    return render(request, 'editar_red_social.html', {'form': form})

def ver_ubicaciones_veterinario(request):

    #veterinarias_queryset = Veterinaria.objects.all()
    #veterinarias_lista = []

    #for veterinaria in veterinarias_queryset:
    #    veterinaria_dict = {
    #        "nombre": veterinaria.nombre,
    #        "calle": veterinaria.calle,
    #        "nro_calle": veterinaria.nro_calle,
    #        "detalle": veterinaria.detalle,
    #        "latitud": veterinaria.latitud,
    #        "longitud": veterinaria.longitud
    #    }
    #    veterinarias_lista.append(veterinaria_dict)

    #return render(request, 'ver_ubicaciones_veterinario.html', {'veterinarias': veterinarias_lista})
    return render(request, 'ver_ubicaciones_veterinario.html')


def editar_ubicacion(request, id_veterinaria):
    return None

def agregar_ubicacion(request):

    if request.method == "POST":
        form = AgregarVeterinaria(request.POST)

        if form.is_valid():
            direccion = f"{form.cleaned_data['calle']} {form.cleaned_data['nro_calle']}, La Plata, Provincia de Buenos Aires"
            api_key = "AIzaSyA5fzRrz8Xx_6BMMpCr5cyGxFZ92u22lnQ"

            url = f'https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={api_key}'
            response = requests.get(url)
            data = response.json()
            
            if data['status'] == 'OK':
                # Obtener la latitud y longitud de la primera ubicación devuelta
                latitud = data['results'][0]['geometry']['location']['lat']
                longitud = data['results'][0]['geometry']['location']['lng']

                veterinaria = Veterinaria(
                    calle=form.cleaned_data['calle'],
                    nro_calle=form.cleaned_data['nro_calle'],
                    detalle=form.cleaned_data['detalle'],
                    longitud=longitud,
                    latitud=latitud
                )
                veterinaria.save()
                messages.success(request, "Veterinaria agregada exitosamente.")
                return redirect('ver_ubicaciones_veterinario')

    form = AgregarVeterinaria()
    return render(request, 'agregar_ubicacion.html', {'form': form})

def get_ubicaciones(request):
    veterinarias = Veterinaria.objects.all().values('latitud', 'longitud')
    serialized_veterinarias = list(veterinarias)

    return JsonResponse({'veterinarias': serialized_veterinarias}, safe=False)


# borrar_ubicacion(request, id_veterinaria):