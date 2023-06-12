from django.shortcuts import render, redirect, HttpResponse
from .models import PerroCruza
from autenticacion.models import CustomUser
from perros.models import Perro
from django.contrib import messages
from .forms import PublicarPerroCruzaForm
from django.core.mail import send_mail

# Create your views here.
def ver_perros_cruza(request):
    perros_cruza = PerroCruza.objects.all()
    return render(request, 'index_cruza.html', 
            {'perros_cruza': perros_cruza}
        )
    
def publicar_perro(request):
    if request.method == "POST":
        form = PublicarPerroCruzaForm(request.POST, request.user)
        if form.is_valid():
            cliente = request.user  
            perro_id = request.POST.get('perro')
            perro = Perro.objects.get(id=perro_id)
            fecha_de_celo = form.cleaned_data['celo']
            perro_cruza = PerroCruza.objects.create(dueño=cliente, perro=perro, fecha_de_celo=fecha_de_celo)
            perro_cruza.save()
            messages.success(request, 'Perro publicado con exito')
            return redirect('ver_perros_cruza')
        else:
          return render(request, 'publicar_perro_cruza.html', {"perros": perros, "form": form})  
    else:
        perros = Perro.objects.filter(dueño=request.user).exclude(id__in=PerroCruza.objects.values('perro_id'))
        form = PublicarPerroCruzaForm()
        return render(request, 'publicar_perro_cruza.html', {"perros": perros, "form": form})
    
def enviar_solicitud_cruce(request, perro, autor, sexo):
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
    perrosCliente = Perro.objects.filter(dueño=request.user)
    return render(request, "enviar_solicitud_cruce.html",{
        "perros": perrosCliente,
        "nombre": perro, 
        "autor": autor,
        "sexo": sexo})